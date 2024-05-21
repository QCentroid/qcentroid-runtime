from .QiskitAbstractProvider import QiskitAbstractProvider

import json
class Qulacs(QiskitAbstractProvider):
    def __init__(self,params):
        self.__params=params
        if "backend" in params:
           self.__backend_name = params.get("backend", "")  
        self._qcentroid_job_id = params.get("qcentroid_job_id", None) 

    def get_provider(self):
        return 'Qulacs'
    def _get_backend(self):
        try:
            from qiskit_qulacs import QulacsProvider        
        except:
            import sys
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'qiskit-qulacs'])
        from qiskit_qulacs import QulacsProvider
        return QulacsProvider().get_backend(self.__backend_name)
                                                        
    def execute(self,circuit):
        backend=self._get_backend()
        job=backend.run(circuit)
        ids={}
        ids['Qulacs Job ID']=job.job_id()
        job.wait_for_final_state()
        if self._qcentroid_job_id is not None:
            with open(str(self._qcentroid_job_id), 'w') as convert_file: 
                convert_file.write(json.dumps(ids))
        return job.get_probabilities()

    
    