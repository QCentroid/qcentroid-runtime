from QiskitAbstractProvider import QiskitAbstractProvider
from qiskit_ibm_runtime import QiskitRuntimeService

class IBMQuantum(QiskitAbstractProvider):
    def get_provider(self):
        return "IBMCloud"
    def __get_service(self):
        if "token" in params:
            self.__token = params.get("IBMCloudToken", "")
        else:
           raise Exception("No token provided") 
        if "instance" in params:
            self.__instance = params.get("IBMCloudInstance", "")
        else:
           raise Exception("No instance provided") 
        return QiskitRuntimeService(channel='ibm_cloud',token=self.__token,instance=self.__instance)