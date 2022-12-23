from typing import BinaryIO, Dict, List, Tuple, Optional
import pickle, hashlib

MBT_size = 1024*1024 # 1 MB

class MasterBootTable:
    def __init__(self, config: str) -> None:
        self.config = MasterBootTable.CONFIG.findall(config)
        self.modified = False

    @classmethod
    def load(cls, file: BinaryIO):
        pointer = file.tell()
        file.seek(0)
        data = file.read(MBT_size)
        file.seek(pointer)
        return cls(pickle.load(data.lstrip(b'0')))
    
    @classmethod
    def make_MBT(cls):
        password = 'installer' # Hash of password is used to encrypt
        for _ in range(2): # Hash of Hash is used for password check
            password = hashlib.sha256(password.encode()).hexdigest()
        config = {'user': 'installer', 
                'password': password,
                'resolution': (1600, 900),
                'file_index': 0
                }
        return cls(config)
    
    def flush(self, file: BinaryIO) -> None:
        file.seek(0)
        file.write(pickle.dumps(self.config).zfill(MBT_size))