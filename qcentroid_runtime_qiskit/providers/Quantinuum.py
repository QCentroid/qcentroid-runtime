from .QiskitAbstractProvider import QiskitAbstractProvider

import json
class Quantinuum(QiskitAbstractProvider):
    def __init__(self,params):
        self.__params=params
        if "backend" in params:
           self.__backend_name = params.get("backend", "")  
        self._qcentroid_job_id = params.get("qcentroid_job_id", None) 

    def get_provider(self):
        return 'Quantinuum'
    def _get_backend(self):
        try:
            from qiskit_quantinuum import Quantinuum
        
        except:
            import sys
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'qiskit-quantinuum-provider'])
            from qiskit_quantinuum import Quantinuum
        import qiskit
        pass
                                                        
    def execute(self,circuit):
        raise Exception('Not implemented')

    
    