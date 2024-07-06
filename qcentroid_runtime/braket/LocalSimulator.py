from .BraketAbstractProvider import BraketAbstractProvider

import json
class LocalSimulator(BraketAbstractProvider):
    def __init__(self,params):
        self.__params=params
        if "backend" in params:
           self.__backend_name = params.get("backend", "")  
        self._qcentroid_job_id = params.get("qcentroid_job_id", None) 

    def get_provider(self):
        return 'LocalSimulator'
    def _get_backend(self):
        try:
            from braket.devices import LocalSimulator
        
        except:
            import sys
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'braket'])
        from braket.devices import LocalSimulator
        return LocalSimulator(backend=self.__backend_name)
                                                        
    def execute(self,circuit):

        shots=self.__params.get('shots',1000)
        device=self._get_backend()
        task=device.run(circuit,shots=shots)
        ids={}
        ids['LocalSimulator Job ID']=task.id
        if self._qcentroid_job_id is not None:
            with open(str(self._qcentroid_job_id), 'w') as convert_file: 
                convert_file.write(json.dumps(ids))
        result = task.result()
        return result.measurement_counts
      
    
    