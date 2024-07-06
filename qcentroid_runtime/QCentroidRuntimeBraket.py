import sys
import logging
import os
logger = logging.getLogger(__name__)
__all__=['braket']
import qcentroid_runtime.braket as providers
from qcentroid_runtime import SingletonMeta
class QCentroidRuntimeBraket(metaclass=SingletonMeta):
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
        provider_name=params.get("provider","LocalSimulator")
        import inspect
        p=[x[1] for x in inspect.getmembers(providers, predicate=inspect.isclass) if x[0]==provider_name]
        if (len(p)==0):
            raise Exception ('Provider: '+provider_name+' is not valid')
        self.__provider=p[0](params)
        
        

    def __init__(self, params=None):
        try:
            import braket
        except:
            import sys
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'braket'])
            import braket
        self.__get_provider(params)

    def execute(self, circuit):
        return self.__provider.execute(circuit)
