from Infinitum.Core.Misc.CONSTANTS import MBT_SIZE

from typing import BinaryIO, Dict

import hashlib
import pickle

def _hash(string: str) -> str:
    return hashlib.sha256(string.encode()).hexdigest()

class MasterBootTable:
    def __init__(self, config: Dict) -> None:
        self.config = config

    @classmethod
    def load(cls, file: BinaryIO) -> 'MasterBootTable':
        file.seek(0)
        data = file.read(MBT_SIZE)
        return pickle.loads(data.lstrip(b'0'))
    
    @classmethod
    def make_MBT(cls, user: str, password: str) -> 'MasterBootTable':
        # Hash of password is used to encrypt
        # Hash of Hash is used for password check
        password = _hash(_hash(password))
        config = {'username': user, 
                'password': password,
                'resolution': (1600, 900),
                'installed': False
                }
        return cls(config)
    
    def flush(self, file: BinaryIO) -> None:
        file.seek(0)
        file.write(pickle.dumps(self).zfill(MBT_SIZE))
    
    def installed(self) -> None:
        self.config['installed'] = True