from typing import ByteString
from hashlib import sha256
import pickle, tempfile, datetime

from Infinitum.Core.Storage.MBT import MasterBootTable as MBT, MBT_size
from Infinitum.Core.Storage.MFT import MasterFileTable as MFT, MFT_size
from Infinitum.Core.Storage.Metadata import Metadata

RESERVED_SPACE = MBT_size + MFT_size

class FileManager:
    def __init__(self, drive_path: str, pwd: str) -> None:
        self.drive, self.working_dir = open(drive_path, 'rb+'), tempfile.TemporaryDirectory()
        self.MBT, self.MFT = MBT.load(self.drive), MFT.load(self.drive)
        #self.temp_dir = tempfile.TemporaryDirectory(dir = self.working_dir)
        key = sha256(pwd.encode()).hexdigest()
        if sha256(key.encode()).hexdigest() != self.MBT.config['password']: raise ValueError('Incorrect Password')
        self.__key = key

    @staticmethod
    def check_install(drive_path: str) -> bool:
        drive = open(drive_path, 'rb+')
        config = MBT.load(drive).config
        return config.get('installed', False)

    @classmethod
    def initial_setup(cls, drive_path: str, username: str, password: str ) -> 'FileManager':
        with open(drive_path, 'wb+') as drive:
            MBT_, MFT_ = MBT.make_MBT(username, password), MFT.make_MFT()
            MBT_.flush(drive); MFT_.flush(drive)
        return cls(drive_path, password)

    # file_path is the location inside the app
    def __create_file(self, file_name: str, file_path: str, binary: bool) -> None:
        index = self.MBT.config['file_index']
        metadata = Metadata(file_name, 0, datetime.now(), index, binary)
        fail = self.MFT.make_file(file_name, metadata, file_path, binary)
        if fail: return 1
        self.MBT.config['file_index'] += 1
        self.MFT.modified = True

    def write(self, data: object | str, metadata: Metadata):
        pointer = sum((self.MFT.index_sizes[i] for i in range(metadata.index))) + RESERVED_SPACE
        self.drive.seek(pointer, 0)
        if not metadata.binary: 
            content = data.encode().zfill(metadata.size)
        else: 
            content = pickle.dumps(data).zfill(metadata.size)
        self.drive.write(self.__encrypt(content))

    def write_open(self, file_name: str, file_path: str | None = None, overwrite = False, binary = False) -> 'BinaryWriteIO | TextWriteIO': 
        if overwrite and self.MFT.exists(file_name, file_path): self.MFT.del_file(file_path)
        self.__create_file(file_name, file_path, binary)
        self.MFT.flush()
        file = self, self.MFT.get_file(file_path, file_name)
        return BinaryWriteIO(*file) if binary else TextWriteIO(*file)
    
    def read_open(self, file_name: str, file_path: str | None = None, binary = False):
        if not self.MFT.exists(file_name, file_path): raise Exception('File Does not Exist')
        file = self, self.MFT.get_file(file_path, file_name)
        return ReadIO(*file) if binary else ReadIO(*file)
    
    def read(self, Bytes: int, metadata: Metadata) -> str:
        pointer = sum((self.MFT.index_sizes[i] for i in range(metadata.index))) + RESERVED_SPACE 
        self.drive.seek(pointer, 0)
        out = self.__decrypt(self.drive.read(Bytes or metadata.size))
        return out.decode() if not metadata.binary else pickle.loads(out)

    def __encrypt(self, data: ByteString) -> ByteString:
        if not self.__key: return data
        result, key = [], 0
        for index in range(len(data)):
            result[index] += ord(self.__key[key])
            key += 1
            if key >= len(self.__key): key = 0
        return pickle.dumps(result)

    def __decrypt(self, data: ByteString) -> ByteString:
        encrypted, decrypted = pickle.loads(data), []
        for index in range(len(encrypted)):
            decrypted[index] -= ord(self.__key[key])
            key += 1
            if key >= len(self.__key): key = 0
        return bytes(decrypted)

    def close(self):
        self.MBT.flush(self.drive)
        self.MFT.flush(self.drive)
        self.drive.close()

def __open__(function): # Decor to check if handle is closed
    def helper(*args, **kwargs):
        obj = args[0]
        if obj.closed: raise Exception('Handle closed')
        return function(*args, **kwargs)
    return helper

class TextWriteIO:
    def __init__(self, manager: FileManager, metadata: Metadata) -> None:
        self.closed = False
        self.data, self.__pointer = '', 0
        self.manager, self.metadata = manager, metadata

    @__open__
    def write(self, data) -> int:
        if not isinstance(data, str): raise TypeError('Must be string object')
        tmp = self.data[:self.tell()] + data + self.data[self.tell()+len(data):]
        if len(tmp) > self.metadata.size: raise OverflowError(f'Contents to be written exceed allocated space by {len(tmp) - self.metadata.size} characters')
        self.data = tmp

    @__open__
    def flush(self):
        self.manager.write(self.data, self.metadata)

    @__open__
    def close(self):
        self.closed = True
        self.flush()

    @__open__
    def tell(self): return self.__pointer

    @__open__
    def seek(self, offset, whence = 0):
        self.__pointer = (offset + whence * self.__pointer) if self.__pointer != 2 else len(self.data) + offset

class BinaryWriteIO:
    def __init__(self, manager: FileManager, metadata: Metadata) -> None:
        self.closed = False
        self.data = b''
        self.manager, self.metadata = manager, metadata

    @__open__
    def write(self, data) -> int:
        tmp = pickle.dumps(data)
        if len(tmp) > self.metadata.size: raise OverflowError('Contents to be written exceed allocated space')
        self.data = data

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
        self.data, self.__pointer = '', 0
        self.manager, self.metadata = manager, metadata
    
    @__open__
    def read(self, Bytes: int = 0):
        if self.__pointer + Bytes > self.metadata.size: raise EOFError('Bytes to read exceed remaining bytes of file')
        self.__pointer += Bytes
        return self.manager.read(self.__pointer, self.metadata)
    
    @__open__
    def tell(self): return self.__pointer

    @__open__
    def seek(self, offset, whence = 0):
        self.__pointer = (offset + whence * self.__pointer) if self.__pointer != 2 else len(self.data) + offset

    @__open__
    def close(self): self.closed = True