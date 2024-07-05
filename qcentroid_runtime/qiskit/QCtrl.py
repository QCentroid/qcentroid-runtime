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
        return 'QCtrl'
    def _get_backend(self):
        
        return self.__backend_name 
    
    def __get_service(self):
        from qiskit_ibm_runtime import QiskitRuntimeService
        if(self._service is not None):
            return self._service
        params=self._get_params()
        if "IBMQuantumToken" in params:
            self.__token = params.get("IBMQuantumToken", "")
        else:
           raise Exception("No token provided") 
        if "IBMQuantumInstance" in params:
            self.__instance = params.get("IBMQuantumInstance", "")
        else:
           raise Exception("No instance provided") 
        self._service= QiskitRuntimeService(channel='ibm_quantum',token=self.__token,instance=self.__instance)
        return self._service

    def __get_credentials(self):
        import fireopal 
        params=self._get_params()
        if "IBMQuantumToken" in params:
            self.__token = params.get("IBMQuantumToken", "")
        else:
           raise Exception("No token provided") 
        if "IBMQuantumInstance" in params:
            self.__instance = params.get("IBMQuantumInstance", "")
        else:
           raise Exception("No instance provided") 
        hub,group,project=self.__instance.split('/')
        credentials = fireopal.credentials.make_credentials_for_ibmq(
            token=self.__token, hub=hub, group=group, project=project
        )
        return credentials
    def execute(self,circuit):
        try:
            import fireopal   
        except:
            import sys
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'fire-opal'])
            import fireopal    
        try:
            import qiskit.qasm3   
        except:
            import sys
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'qiskit-qasm3-import'])
            import qiskit.qasm3  
        from qiskit.primitives import SamplerResult
        fireopal.configure_organization(self.__params.get('FIREOPAL_ORGANIZATION',''))
        fireopal.authenticate_qctrl_account(self.__params.get('FIREOPAL_TOKEN',''))
        service=self.__get_service()
        credentials=self.__get_credentials()
        backend=self._get_backend()
        shots=self.__params.get('shots',1000)
        circuit_qasm=qiskit.qasm3.dumps(circuit)        
        job=fireopal.execute(circuits=[circuit_qasm],shot_count=shots,credentials=credentials,backend_name=backend)
        ids={}
        ids['FireOpal Job ID']=job.action_id
        if self._qcentroid_job_id is not None:
            with open(str(self._qcentroid_job_id), 'w') as convert_file: 
                convert_file.write(json.dumps(ids))
        r= {int(x,2):y for x,y in job.result()['results'][0].items()}
        return SamplerResult([r],[{'shots':shots}])
    
    
