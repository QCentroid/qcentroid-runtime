from .QiskitAbstractProvider import QiskitAbstractProvider

import qiskit
import json
class AQT(QiskitAbstractProvider):
    def __init__(self,params):
        self.__params=params
        if "backend" in params:
           self.__backend_name = params.get("backend", "")  
        self._qcentroid_job_id = params.get("qcentroid_job_id", None) 

    def get_provider(self):
        return 'AQT'
    def _get_backend(self):
        from qiskit_aqt_provider import AQTProvider
        provider = AQTProvider(self.__params.get('AQT_AccessToken',"ACCESS_TOKEN"))
        backend=provider.get_backend(self.__backend_name)
        return backend
                                                        
    def execute(self,circuit):
        try:
            from qiskit_aqt_provider.primitives import AQTSampler        
        except:
            import sys
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'qiskit-aqt-provider'])
            from qiskit_aqt_provider.primitives import AQTSampler        
        from qiskit.primitives import SamplerResult
        backend=self._get_backend()
        shots=self.__params.get('shots',1000)
        sampler=AQTSampler(backend)
        sampler.set_transpile_options(optimization_level=3)
        job=sampler.run(circuit,shots=shots)
        ids={}
        ids['AQT Job ID']=job.job_id()
        if self._qcentroid_job_id is not None:
            with open(str(self._qcentroid_job_id), 'w') as convert_file: 
                convert_file.write(json.dumps(ids))
        return SamplerResult([job.result().quasi_dists[0]],[{'shots':shots}])

    
    