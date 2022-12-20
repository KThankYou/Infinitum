from typing import BinaryIO, Dict, List, Optional
import pickle

from Infinitum.Core.Storage.MBT import MBT_size
from Infinitum.Core.Storage.Metadata import Metadata

MFT_size = 10*1024*1024 # 10 MB

class MasterFileTable:
    def __init__(self, MFT: Dict) -> None:
        self.__table = MFT
        self.__cwd = ('root', MFT['root'])
        self.__path = ['.']

    @classmethod
    def load(cls, file: BinaryIO):
        pointer = file.tell()
        file.seek(MBT_size, 0)
        data = file.read(MFT_size)
        file.seek(pointer)
        return cls(pickle.load(data.lstrip(b'0')))
    
    @classmethod
    def make_MFT(cls):
        table = {'root': 
            {'Apps': {'__files': {}}, 
            'User': {'__files': {}}, 
            '__files': {}}}
        return cls(table)
    
    def flush(self, file: BinaryIO) -> None:
        file.seek(MBT_size, 0)
        file.write(pickle.dumps(self.__table).zfill(MFT_size))

    #Return None if successful, 1 if fail
    def make_dir(self, folder_name: str) -> Optional[1]:
        if folder_name in self.__cwd[1]: return 1
        self.__cwd[1][folder_name] = {'__files':{}}

    def del_dir(self, folder_name: str) -> Optional[1]:
        if folder_name not in self.__cwd[1]: return 1
        del self.__cwd[1][folder_name]

    def cd(self, folder: str):
        if folder not in self.__cwd[1]: return 1
        self.__cwd = self.__cwd[1][folder]
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

    def make_file(self, file_name: str, meta_link: Metadata, location: str = None) -> Optional[1]:
        c_dir, c_path = self.__cwd, self.__path
        if location: self.set_cwd(location)
        folder = self.__cwd[1]['__files']
        self.__cwd, self.__path = c_dir, c_path
        if file_name in folder: return 1
        folder['__files'][file_name] = meta_link
        
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