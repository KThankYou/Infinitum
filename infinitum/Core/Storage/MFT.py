from typing import BinaryIO, Dict, List, Optional
import pickle

from Infinitum.Core.Storage.MBT import MBT_size
from Infinitum.Core.Storage.Metadata import Metadata

MFT_size = 1*1024*1024 # 1 MB

def modified(function):
    def helper(*args, **kwargs):
        res = function(*args, **kwargs)
        args[0].modified = True
        return res
    return helper

class MasterFileTable:
    def __init__(self, MFT: Dict, indices: Dict[int, int]) -> None:
        self.__table = MFT
        self.__cwd = ('root', MFT['root'])
        self.__path = ['.']
        self.modified = False
        self.index_sizes = indices

    @classmethod
    def load(cls, file: BinaryIO) -> 'MasterFileTable':
        pointer = file.tell()
        file.seek(MFT_size, 0)
        data = file.read(MFT_size)
        file.seek(pointer)
        try: return cls(*pickle.loads(data.lstrip(b'0')))
        except: return cls({'root':{}}, {})
    
    @classmethod
    def make_MFT(cls) -> 'MasterFileTable':
        table = {'root': 
            {'Apps': {'__files': {}}, 
            'User': {'__files': {}}, 
            '__files': {}}}
        obj = cls(table, {})
        obj.modified = True
        return obj
    
    def flush(self, file: BinaryIO) -> None:
        if self.modified:
            file.seek(MFT_size, 0)
            file.write(pickle.dumps([self.__table, self.index_sizes]).zfill(MFT_size))
            self.modified = False
        else: return 1

    #Return None if successful, 1 if fail
    @modified
    def make_dir(self, folder_name: str) -> Optional[1]:
        if folder_name in self.__cwd[1]: return 1
        self.__cwd[1][folder_name] = {'__files':{}}

    @modified
    def del_dir(self, folder_name: str) -> Optional[1]:
        if folder_name not in self.__cwd[1]: return 1
        del self.__cwd[1][folder_name]

    def cd(self, folder: str):
        if folder not in self.__cwd[1]: return 1
        self.__cwd = folder, self.__cwd[1][folder]
        self.__path.append(folder)

    def set_cwd(self, directory: str) -> Optional[1]:
        c_dir, c_path, self.__cwd = self.__cwd, self.__path, self.__table['root'] # c_ means current path
        directory = MasterFileTable.parse_path(directory)
        for i in directory:
            if self.cd(i): 
                self.__cwd, self.__path = c_dir, c_path
                return 1
        
    @property
    def get_cwd(self) -> str: return '\\'.join(self.__path)

    @modified
    def make_file(self, file_name: str, metadata: Metadata, file_path: str) -> Optional[1]:
        c_dir, c_path = self.__cwd, self.__path
        if file_path: self.set_cwd(file_path)
        folder = self.__cwd[1]['__files']
        self.__cwd, self.__path = c_dir, c_path
        if file_name in folder: return 1
        folder['__files'][file_name] = metadata
        self.index_sizes[metadata.index] = metadata.size
    
    def exists(self, file_name: str, file_path: str | None) -> bool:
        c_dir, c_path = self.__cwd, self.__path
        if self.set_cwd(file_path): return False
        if file_name in self.__cwd['__files']: self.__cwd, self.__path = c_dir, c_path; return True
    
    def get_file(self, file_name: str, file_path: str) -> Metadata:
        c_dir, c_path = self.__cwd, self.__path
        if self.set_cwd(file_path) or file_name not in self.__cwd[1]['__files']: 
            self.__cwd, self.__path
            raise ValueError('File/Directory does not exist')
        metadata, self.__cwd, self.__path = self.__cwd[1]['__files'][file_name], c_dir, c_path
        return metadata

    @modified
    def del_file(self, file_path: str) -> Optional[1]:
        c_dir, c_path = self.__cwd, self.__path
        *path, file = MasterFileTable.parse_path(file_path)
        self.set_cwd(path[:-1])
        folder, self.__cwd, self.__path = self.__cwd[1]['__files'], c_dir, c_path
        if file not in folder: return 1
        del folder[file]

    def parse_path(self, path: str) -> List[str]:
        raw = path.split('\\')
        if raw[0] == '.': raw = self.__path[1:] + raw[1:]
        return raw

    @staticmethod
    def join(*args):
        return '\\'.join((i.rstrip('\\') for i in args))