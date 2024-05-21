from .QiskitAbstractProvider import QiskitAbstractProvider

import json
class IQM(QiskitAbstractProvider):
    def __init__(self,params):
        self.__params=params
        if "backend" in params:
           self.__backend_name = params.get("backend", "")  
        self._qcentroid_job_id = params.get("qcentroid_job_id", None) 

    def get_provider(self):
        return 'IQM'
    def _get_backend(self):
        try:
            from iqm import qiskit_iqm
        
        except:
            import sys
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'qiskit-iqm'])
            from iqm import qiskit_iqm
        
        from iqm.qiskit_iqm import IQMProvider
        import qiskit
        pass
                                                        
    def execute(self,circuit):
        raise "Not implemented"
    
    