import sys
import logging
import os
logger = logging.getLogger(__name__)
__all__=['providers']

import qcentroid_runtime_qiskit.providers as providers
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class QCentroidRuntimeQiskit(metaclass=SingletonMeta):
    _singleton = None

    @staticmethod
    def getVersion() -> str:
        # compatible with python 3.7 version
        if sys.version_info >= (3, 8):
            from importlib import metadata
        else:
            import importlib_metadata as metadata

        if __name__:
            return metadata.version(__name__)

        return "unknown"

    def __get_provider(self,params):
        provider_name=params.get("provider","IBMQuantum")
        import inspect
        p=[x[1] for x in inspect.getmembers(providers, predicate=inspect.isclass) if x[0]==provider_name]
        if (len(p)==0):
            raise Exception ('Provider: '+provider_name+' is not valid')
        self.__provider=p[0](params)
        
        

    def __init__(self, params=None):
        try:
            import qiskit
        except:
            import sys
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'qiskit'])
            import qiskit
        self.__get_provider(params)

    def execute(self, circuit):
        return self.__provider.execute(circuit)


    
__all__ = ["QCentroidRuntimeQiskit"]
