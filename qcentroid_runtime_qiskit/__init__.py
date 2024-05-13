from requests_toolbelt import MultipartEncoder
import requests
from requests.exceptions import HTTPError
import json
import os
import mimetypes
from io import StringIO
from qcentroid_runtime_qiskit.model import Status, StatusEntity
import sys
import ssl
import logging

logger = logging.getLogger(__name__)

class QCentroidRuntimeQiskit():    
    _singleton = None
    _token = None
    _instance = None
    
    @staticmethod
    def getVersion()->str:
        # compatible with python 3.7 version
        if sys.version_info >= (3, 8):
            from importlib import metadata
        else:
            import importlib_metadata as metadata

        if __name__:
            return metadata.version(__name__)
    
        return "unknown"
    
    
    def __init__(self):
        raise RuntimeError('Call configure() instead')
    @classmethod
    def configure(cls, params:dict={}):
        if cls._singleton is None:
            print('Creating new instance')
            cls._singleton = cls.__new__(cls)
            # Put any initialization here.
            if params:
                if "token" in params:
                  cls._token =  dict["token"]
                if "instance" in params:
                  cls._instance =  dict["instance"]
        return cls._instance
    @classmethod
    def execute(cls, circuit):
        #TODO write execution code
        pass            

            
__all__ = ['QCentroidRuntimeQiskit']
