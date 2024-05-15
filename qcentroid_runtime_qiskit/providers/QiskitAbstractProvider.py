try:
    import qiskit_ibm_runtime
except:
    import sys
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'qiskit_ibm_runtime'])
    import qiskit_ibm_runtime
    
from abc import ABC, abstractmethod
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import Sampler,Session
from qiskit_ibm_runtime import QiskitRuntimeService
import json

class QiskitAbstractProvider(ABC):
    @abstractmethod
    def get_provider(self):
        pass
        
    @abstractmethod   
    def _get_service(self):
        pass
    
    def __init__(self,params):
        self._params=params
        if "backend" in params:
           self.__backend_name = params.get("backend", "") 
        self.__qcentroid_job_id = None    
        self.__qcentroid_job_id = params.get("qcentroid_job_id", None) 

    
    def __get_backend(self):
        
        
        #recuperar de env el backend
        from qiskit_ibm_runtime.fake_provider import FakeAlmadenV2
        return FakeAlmadenV2()

        #return self.__service.least_busy()



    
    def execute(self,circuit):
        ids={}
        
        self.__service = self._get_service()
        backend = self.__get_backend()
        session=Session(service=self.__service,backend=backend)
        ids['Session']=session.session_id
        
        
        pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
        isa_qc = pm.run(circuit)
        sampler = Sampler(backend=backend,session=session)
        #recuperar hiperparametros de la ejecución
        shots=1000 #hyperparameters.getparameter('shots')
        job=sampler.run(isa_qc,shots=shots)
        ids['Job']=job.job_id()
        if self.__qcentroid_job_id is not None:
            with open(str(self.__qcentroid_job_id), 'w') as convert_file: 
                convert_file.write(json.dumps(ids))
        #insertar la relacion entre QCentroidJob y IBMJob
        result=job.result()
        return result