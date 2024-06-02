from .QiskitAbstractProvider import QiskitAbstractProvider

import json
class IonQ(QiskitAbstractProvider):
    def __init__(self,params):
        self.__params=params
        if "backend" in params:
           self.__backend_name = params.get("backend", "")  
        self._qcentroid_job_id = params.get("qcentroid_job_id", None) 

    def get_provider(self):
        return 'IonQ'
    def _get_backend(self):
        try:
            from qiskit_ionq import IonQProvider
        except:
            import sys
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'qiskit-ionq'])
            from qiskit_ionq import IonQProvider
        
        provider = IonQProvider(token=self.__params.get('IonQ_API_Key',""))
        backend=provider.get_backend(self.__backend_name)
        backend.options.noise_model=self.__params.get('IonQ_Noise_Model',"ideal")
        return backend
                                                        
    def execute(self,circuit):
        from qiskit.primitives import SamplerResult
        shots=self.__params.get('shots',1000)
        backend=self._get_backend()
        backend.set_options(**{'shots':shots})
        job=backend.run(circuit)
        ids={}
        ids['IonQ Job ID']=job.job_id()
        job.wait_for_final_state()
        if self._qcentroid_job_id is not None:
            with open(str(self._qcentroid_job_id), 'w') as convert_file: 
                convert_file.write(json.dumps(ids))
        r= {int(x,2):y for x,y in job.get_probabilities().items()}
        return SamplerResult([r],[{'shots':shots}])

    
    