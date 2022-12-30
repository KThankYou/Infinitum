from Infinitum.Core.Storage.MFT import MasterFileTable as MFT, MFT_size, BLOCKSIZE
from Infinitum.Core.Storage.MBT import MasterBootTable as MBT, MBT_size
from Infinitum.Core.Storage.Metadata import Metadata
from typing import Tuple, Dict
from hashlib import sha256
from math import ceil
import pickle, tempfile

RESERVED_SPACE = MBT_size + MFT_size

class FileManager:
    def __init__(self, drive_path: str, pwd: str) -> None:
        self.drive, self.working_dir = open(drive_path, 'rb+'), tempfile.TemporaryDirectory()
        self.MBT, self.MFT = MBT.load(self.drive), MFT.load(self.drive)
        key = sha256(pwd.encode()).hexdigest()
        if sha256(key.encode()).hexdigest() != self.MBT.config['password']: raise ValueError('Incorrect Password')
        self.__key = key

    def temp(self): 
        return tempfile.TemporaryDirectory(dir = self.working_dir.name)

    @staticmethod
    def check_install(drive_path: str) -> bool:
        config = FileManager.get_config(drive_path)
        return config.get('installed', False)

    @staticmethod
    def get_user(drive_path: str) -> str:
        config = FileManager.get_config(drive_path)
        return config.get('username', '')
    
    @staticmethod
    def get_pwd(drive_path: str) -> str:
        config = FileManager.get_config(drive_path)
        return config.get('password', '')
    
    @staticmethod
    def get_config(drive_path: str) -> Dict:
        with open(drive_path, 'rb') as drive:
            config = MBT.load(drive).config
        return config

    @staticmethod
    def get_res(drive_path: str) -> Tuple[int, int]:
        config = FileManager.get_config(drive_path)
        return config.get('resolution', '')

    @classmethod
    def initial_setup(cls, drive_path: str, username: str, password: str ) -> 'FileManager':
        with open(drive_path, 'wb+') as drive:
            MBT_, MFT_ = MBT.make_MBT(username, password), MFT.make_MFT()
            MBT_.flush(drive); MFT_.flush(drive)
        return cls(drive_path, password)

    # file_path is the location inside the app
    def __create_file(self, file_name: str, file_path: str, binary: bool) -> None:
        metadata = self.MFT.make_metadata(0, file_name, binary)
        fail = self.MFT.make_file(file_name, metadata, file_path)
        if fail: return 1

    def write(self, data: object | str, metadata: Metadata) -> None:
        node, data = metadata.head, pickle.dumps(data)
        data = self.__encrypt(data)
        blocks = ceil(len(data)//BLOCKSIZE)*BLOCKSIZE
        data = data.zfill(blocks)
        if metadata.size < len(data): self.MFT.update_size(metadata, len(data))
        for size in range(0, blocks, BLOCKSIZE):
            self.drive.seek(RESERVED_SPACE + node.pointer, 0)
            self.drive.write(data[size:size+BLOCKSIZE])
            node = node.next
        return data.decode() if not metadata.binary else pickle.loads(data)

    def write_open(self, file_name: str, file_path: str = None, binary: bool = False) -> 'WriteIO': 
        if self.MFT.exists(file_name, file_path): self.MFT.del_file(file_path)
        self.__create_file(file_name, file_path, binary)
        self.MFT.flush()
        file = self, self.MFT.get_file(file_path, file_name)
        return WriteIO(*file)
    
    def read_open(self, file_name: str, file_path: str = None) -> 'ReadIO':
        if not self.MFT.exists(file_name, file_path): raise Exception('File Does not Exist')
        file = self, self.MFT.get_file(file_path, file_name)
        return ReadIO(*file)
    
    def read(self, metadata: Metadata) -> str | object:
        node, data = metadata.head, b''
        while node:
            data += self.__read_bytes(BLOCKSIZE, RESERVED_SPACE + node.pointer)
            node = node.next
        data = self.__decrypt(data)
        return data.decode() if not metadata.binary else pickle.loads(data)
    
    def __read_bytes(self, Bytes: int, pointer: int) -> bytes:
        self.drive.seek(pointer, 0)
        return self.drive.read(Bytes)

    def __encrypt(self, data: bytes) -> bytes:
        result, key = [], 0
        for index in range(len(data)):
            result[index] += ord(self.__key[key])
            key += 1
            if key >= len(self.__key): key = 0
        return pickle.dumps(result)

    def __decrypt(self, data: bytes) -> bytes:
        encrypted, decrypted = pickle.loads(data), []
        for index in range(len(encrypted)):
            decrypted[index] -= ord(self.__key[key])
            key += 1
            if key >= len(self.__key): key = 0
        return bytes(decrypted)

    def close(self):
        self.MBT.flush(self.drive)
        self.MFT.flush(self.drive)
        self.working_dir.cleanup()
        self.drive.close()

def __open__(function): # Decor to check if handle is closed
    def helper(*args, **kwargs):
        obj = args[0]
        if obj.closed: raise Exception('Handle closed')
        return function(*args, **kwargs)
    return helper

class WriteIO:
    def __init__(self, manager: FileManager, metadata: Metadata) -> None:
        self.closed = False
        self.manager, self.metadata = manager, metadata

    @__open__
    def write(self, data: object) -> int:
        return self.manager.write(data, self.metadata)

    @__open__
    def flush(self):
        self.manager.write(self.data, self.metadata)

    @__open__
    def close(self):
        self.closed = True
        self.flush()

class ReadIO:
    def __init__(self, manager: FileManager, metadata: Metadata) -> None:
        self.closed = False
        self.manager, self.metadata = manager, metadata
    
    @__open__
    def read(self):
        return self.manager.read(self.metadata)
        
    @__open__
    def close(self): self.closed = True
