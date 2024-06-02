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
        from qiskit.primitives import SamplerResult
        shots=self.__params.get('shots',1000)
        backend=self._get_backend()
        backend.set_options(**{'shots':shots})
        job=backend.run(circuit)
        ids={}
        ids['Qulacs Job ID']=job.job_id()
        job.wait_for_final_state()
        if self._qcentroid_job_id is not None:
            with open(str(self._qcentroid_job_id), 'w') as convert_file: 
                convert_file.write(json.dumps(ids))
        r= {int(x,2):y/shots for x,y in job.result().get_counts().items()}
        return SamplerResult([r],[{'shots':shots}])

    
    