from .QiskitAbstractProvider import QiskitAbstractProvider

import json
class AliceBob(QiskitAbstractProvider):
    def __init__(self,params):
        self.__params=params
        if "backend" in params:
           self.__backend_name = params.get("backend", "")  
        self._qcentroid_job_id = params.get("qcentroid_job_id", None) 

    def get_provider(self):
        return 'Alice&Bob'
    def _get_backend(self):
        try:
            from qiskit_alice_bob_provider import AliceBobLocalProvider
        
        except:
            import sys
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'qiskit-alice-bob-provider'])
        from qiskit_alice_bob_provider import AliceBobLocalProvider
        from qiskit_alice_bob_provider import AliceBobRemoteProvider
        import qiskit
        pass
                                                        
    def execute(self,circuit):
        raise Exception('Not implemented')

    
    