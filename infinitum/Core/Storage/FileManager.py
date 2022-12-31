from Infinitum.CONSTANTS import MFT_SIZE, MBT_SIZE, BLOCKSIZE, RESERVED_SPACE
from Infinitum.Core.Storage.MFT import MasterFileTable as MFT
from Infinitum.Core.Storage.MBT import MasterBootTable as MBT
from Infinitum.Core.Storage.Metadata import Metadata

from typing import Tuple, Dict, BinaryIO
from hashlib import sha256
from math import ceil

import tempfile
import pickle


class FileManager:
    def __init__(self, drive_path: str, pwd: str) -> None:
        self.drive, self.working_dir = open(drive_path, 'rb+'), tempfile.TemporaryDirectory()
        key, self.MBT = sha256(pwd.encode()).hexdigest(), MBT.load(self.drive)
        if sha256(key.encode()).hexdigest() != self.MBT.config['password']: raise ValueError('Incorrect Password')
        self.key = key
        self.MFT = MFT.load(self)

    def temp(self) -> tempfile.TemporaryDirectory: 
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
            MBT_.flush(drive); MFT_.flush(FileManager, drive, sha256(password.encode()).hexdigest())
        return cls(drive_path, password)

    # file_path is the location inside the app
    def __create_file(self, file_name: str, file_path: str) -> None:
        metadata = self.MFT.make_metadata(0, file_name)
        fail = self.MFT.make_file(file_name, metadata, file_path)
        if fail: return 1

    def write(self, obj: object, metadata: Metadata) -> None:
        node, raw_data = metadata.head, pickle.dumps(obj)
        data = FileManager.encrypt(raw_data, self.key)
        blocks = ceil(len(data)/BLOCKSIZE)*BLOCKSIZE
        data = data.zfill(blocks)
        if metadata.size < len(data): self.MFT.update_size(metadata, len(data))
        for size in range(0, blocks, BLOCKSIZE):
            self.drive.seek(RESERVED_SPACE + node.pointer, 0)
            self.drive.write(data[size:size+BLOCKSIZE])
            node = node.next

    @staticmethod
    def write_MFT(drive: BinaryIO, pwd: str, obj: object):
        data = FileManager.encrypt(pickle.dumps(obj), pwd = pwd)
        drive.seek(MBT_SIZE, 0)
        drive.write(data.zfill(MFT_SIZE))
        drive.flush()

    @staticmethod
    def read_MFT(drive: BinaryIO, pwd: str) -> MFT:
        drive.seek(MBT_SIZE, 0)
        encrypted = drive.read(MFT_SIZE)
        data = FileManager.decrypt(encrypted.strip(b'0'), pwd)
        return pickle.loads(data)

    def write_open(self, file_name: str, file_path: str = '') -> 'WriteIO': 
        if self.MFT.exists(file_name, file_path): self.MFT.del_file(file_path)
        self.__create_file(file_name, file_path)
        self.MFT.flush(self, self.drive, password=self.key)
        file = self, self.MFT.get_file(file_name, file_path)
        return WriteIO(*file)
    
    def read_open(self, file_name: str, file_path: str = '') -> 'ReadIO':
        if not self.MFT.exists(file_name, file_path): raise Exception('File Does not Exist')
        file = self, self.MFT.get_file(file_name, file_path)
        return ReadIO(*file)
    
    def read(self, metadata: Metadata) -> object:
        node, data = metadata.head, b''
        while node:
            data += self.__read_bytes(BLOCKSIZE, RESERVED_SPACE + node.pointer)
            node = node.next
        data = self.decrypt(data.lstrip(b'0'), self.key)
        return pickle.loads(data)
    
    def __read_bytes(self, Bytes: int, pointer: int) -> bytes:
        self.drive.seek(pointer, 0)
        return self.drive.read(Bytes)

    @staticmethod
    def encrypt(data: bytes, pwd: str) -> bytes:
        result, key = list(data), 0
        for index in range(len(result)):
            result[index] += ord(pwd[key])
            key += 1
            if key >= len(pwd): key = 0
        return pickle.dumps(result)

    @staticmethod
    def decrypt(data: bytes, pwd: str) -> bytes:
        decrypted, key = list(pickle.loads(data)), 0
        for index in range(len(decrypted)):
            decrypted[index] -= ord(pwd[key])
            key += 1
            if key >= len(pwd): key = 0
        return bytes(decrypted)

    def flush(self) -> None:
        self.MBT.flush(self.drive)
        self.MFT.flush(self, self.drive, self.key)
        self.drive.flush()

    def close(self) -> None:
        self.flush()
        self.working_dir.cleanup()
        self.drive.close()

    def make_folder(self, folder_name: str, folder_path: str, overwrite: bool = False) -> str:
        path = self.MFT.make_dir(folder_name, folder_path)
        if path == 1: 
            if not overwrite: raise Exception('Folder already exists')
            self.del_folder(folder_name, folder_path)
            path = self.MFT.make_dir(folder_name, folder_path)
        return path
    
    def del_folder(self, folder_name: str, folder_path: str) -> None:
        self.MFT.del_dir(folder_name, folder_path)
    
    def get_apps(self) -> Dict[str, Metadata]:
        return self.MFT.get_apps()

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
        self.manager.flush()

    @__open__
    def close(self):
        self.flush()
        self.closed = True

class ReadIO:
    def __init__(self, manager: FileManager, metadata: Metadata) -> None:
        self.closed = False
        self.manager, self.metadata = manager, metadata
    
    @__open__
    def read(self):
        return self.manager.read(self.metadata)
        
    @__open__
    def close(self): self.closed = True
