import datetime

class Metadata:
    def __init__(self, name: str, size: int, date_mod: datetime.datetime, index: int) -> None:
        self.__name, self.__size, self.__date_mod = name, size, date_mod
        self.__index = index

    @property
    def name(self): return self.__name
    @property
    def size(self): return self.__size
    @property
    def date_mod(self): return self.__date_mod
    @property
    def index(self): return self.__index