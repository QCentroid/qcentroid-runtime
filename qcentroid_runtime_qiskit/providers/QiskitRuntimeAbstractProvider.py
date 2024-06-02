from .QiskitAbstractProvider import QiskitAbstractProvider
from abc import ABC, abstractmethod

import json

class QiskitRuntimeAbstractProvider(QiskitAbstractProvider):
    __LOCAL_PROVIDER=0
    __REMOTE_PROVIDER=1
    _service=None
    @abstractmethod
    def get_provider(self):
        pass
        
    @abstractmethod   
    def _get_service(self):
        pass
    
    def __init__(self,params):
        self.__params=params
        if "backend" in params:
           self.__backend_name = params.get("backend", "")  
        self._qcentroid_job_id = params.get("qcentroid_job_id", None) 

    def _get_params(self):
        return self.__params

    def _get_backend(self):        
        params=self._get_params()
        if(params.get('backend','').startswith('ibm') or params.get('backend','').startswith('simulator')):
            return self._get_service().backend(params.get('backend','')),self.__REMOTE_PROVIDER
        elif (params.get('backend','').startswith('Fake')):
            import inspect
            import  qiskit_ibm_runtime.fake_provider as fake
            backends=[x[1] for x in inspect.getmembers(fake,  predicate=inspect.isclass) if x[0]==params.get('backend','')]
            if len(backends)>0:
                return backends[0](),self.__LOCAL_PROVIDER
        raise Exception('Backend '+params.get('backend','')+' not supported')



    
    def execute(self,circuit):
        try:
            import qiskit_ibm_runtime
        except:
            import sys
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'qiskit-ibm-runtime'])
            import qiskit_ibm_runtime
        from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
        from qiskit_ibm_runtime import Sampler,Session
        from qiskit_ibm_runtime import QiskitRuntimeService
        ids={}
        backend,backend_type = self._get_backend()
        shots=self.__params.get('shots',1000)
        if(backend_type==self.__REMOTE_PROVIDER):
            self.__service = self._get_service()
            
            session=Session(service=self.__service,backend=backend)
            ids['Session']=session.session_id
            
            
            pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
            isa_qc = pm.run(circuit)
            sampler = Sampler(backend=backend,session=session)
            #recuperar hiperparametros de la ejecución
            
            job=sampler.run(isa_qc,shots=shots)
            ids['Job']=job.job_id()
            if self._qcentroid_job_id is not None:
                with open(str(self._qcentroid_job_id), 'w') as convert_file: 
                    convert_file.write(json.dumps(ids))
            #insertar la relacion entre QCentroidJob y IBMJob
            result=job.result()
            return result
        else:
            from qiskit.primitives import SamplerResult
            ids['Session']='LOCAL'
            backend.set_options(**{'shots':shots})
            job=backend.run(circuit)
            ids['Job']=job.job_id()
            if self._qcentroid_job_id is not None:
                with open(str(self._qcentroid_job_id), 'w') as convert_file: 
                    convert_file.write(json.dumps(ids))
            res=job.result()
            r={int(x, 2):y/shots for x,y in list(res.get_counts().items())}
            return SamplerResult([r],[{'shots':shots}])