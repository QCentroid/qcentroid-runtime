from .QiskitAbstractProvider import QiskitAbstractProvider

import json
class Rigetti(QiskitAbstractProvider):
    def __init__(self,params):
        self.__params=params
        if "backend" in params:
           self.__backend_name = params.get("backend", "")  
        self._qcentroid_job_id = params.get("qcentroid_job_id", None) 

    def get_provider(self):
        return 'Rigetti'
    def _get_backend(self):
        try:
            from qiskit_rigetti import RigettiQCSProvider   
        except:
            import sys
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'qiskit-rigetti'])
        from qiskit_rigetti import RigettiQCSProvider
        provider = RigettiQCSProvider()
        backend = provider.get_simulator(num_qubits=2, noisy=True) 
        return backend
                                                        
    def execute(self,circuit):
        raise Exception('Waiting to new version')
        backend=self._get_backend()
        job=backend.run(circuit)
        ids={}
        ids['Rigetti Job ID']=job.job_id()
        job.wait_for_final_state()
        if self._qcentroid_job_id is not None:
            with open(str(self._qcentroid_job_id), 'w') as convert_file: 
                convert_file.write(json.dumps(ids))
        return job.get_probabilities()

    
    