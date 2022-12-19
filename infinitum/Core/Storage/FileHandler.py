from typing import BinaryIO, Dict
import datetime, pickle, json

class Metadata:
    def __init__(self, name: str, parent, size: int, date_mod: datetime.datetime, index: int) -> None:
        self.__name, self.__parent, self.__size, self.__date_mod = name, parent, size, date_mod
        self.__index = index

    @property
    def name(self): return self.__name
    @property
    def parent(self): return self.__parent
    @property
    def size(self): return self.__size
    @property
    def date_mod(self): return self.__date_mod
    @property
    def index(self): return self.__index

class MasterFileTable:
    def __init__(self, table: Dict) -> None:
        self.__table = table

    @classmethod
    def from_vd(cls, file: BinaryIO):
        pointer = file.tell()
        file.seek(5242880, 0)
        data = file.read(15728640)
        file.seek(pointer)
        return cls(pickle.load(data.lstrip(b'0')))
        
    @classmethod
    def create_table(cls):
        table = {'root': {'Apps':{}, 'User':{}}}
        return cls(table)
    
    def flush(self, file: BinaryIO) -> None:
        file.write(pickle.dumps(self.__table).zfill(157286400))

    def pretty_print(self):
        pass

