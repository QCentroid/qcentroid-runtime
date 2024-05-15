from .QiskitAbstractProvider import QiskitAbstractProvider
from qiskit_ibm_runtime import QiskitRuntimeService

class IBMQuantum(QiskitAbstractProvider):
    def __init__(self,params):
        self.__params=params
        super().__init__(params)
    def get_provider(self):
        return "IBMQuantum"
    def _get_service(self):
        print(self.__params)
        params=self.__params
        if "IBMQuantumToken" in params:
            self.__token = params.get("IBMQuantumToken", "")
        else:
           raise Exception("No token provided") 
        if "IBMQuantumInstance" in params:
            self.__instance = params.get("IBMQuantumInstance", "")
        else:
           raise Exception("No instance provided") 
        return QiskitRuntimeService(channel='ibm_quantum',token=self.__token,instance=self.__instance)