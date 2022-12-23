import datetime

class Metadata: #Default size allocated for a single file is 5mb
    def __init__(self, name: str, date_mod: datetime.datetime, index: int, binary: bool, size: int = 1024*1024*5) -> None:
        self.__name, self.__size, self.__date_mod = name, size, date_mod
        self.__index, self.__binary = index, binary

    @property
    def name(self): return self.__name
    @property
    def size(self): return self.__size
    @property
    def date_mod(self): return self.__date_mod
    @property
    def index(self): return self.__index
    @property
    def binary(self): return self.__binary