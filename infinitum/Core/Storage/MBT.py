from typing import BinaryIO, Dict
import pickle, hashlib

MBT_size = 1024*1024//2 # 0.5 MB

class MasterBootTable:
    def __init__(self, config: Dict) -> None:
        self.config = config

    @classmethod
    def load(cls, file: BinaryIO):
        pointer = file.tell()
        file.seek(0)
        data = file.read(MBT_size)
        file.seek(pointer)
        try: return cls(pickle.loads(data.lstrip(b'0')))
        except: return cls({'installed': False})
    
    @classmethod
    def make_MBT(cls, user: str, password: str):
        # Hash of password is used to encrypt
        for _ in range(2): # Hash of Hash is used for password check
            password = hashlib.sha256(password.encode()).hexdigest()
        config = {'user': user, 
                'password': password,
                'resolution': (1600, 900),
                'file_index': 0,
                'installed': False
                }
        return cls(config)
    
    def flush(self, file: BinaryIO) -> None:
        file.seek(0)
        file.write(pickle.dumps(self.config).zfill(MBT_size))
    
    def installed(self) -> None:
        self.config['installed'] = True