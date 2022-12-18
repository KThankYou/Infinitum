from typing import Callable, Dict, Tuple, Optional
from Infinitum.Core.Threading import Process

class ThreadHandler:
    def __init__(self) -> None:
        self.__sudo, self.__sudo_pid = {0: Reserved}, 0
        self.__children, self.__pid = {10000: Reserved}, 10000

    def is_alive(self, pid: int) -> bool:
        if pid < 10000: return self.__sudo.get(pid, 0).is_started()

    def create_process(self, function: Callable, sudo: bool = False, *args: Optional[Tuple], **kwargs: Optional[Dict]) -> Process:
        pid = self.__makePID(sudo)
        process = Process.Process(function, args, kwargs)
        if sudo: self.__sudo[pid] = process
        else: self.__children[pid] = process
        return process

    def __makePID(self, sudo: Optional[bool] = False) -> int:
        if sudo:
            self.__sudo_pid += 1
            return self.__sudo_pid
        self.__pid += 1
        return self.__pid

class Reserved:
    is_started = False

    def __init__(self) -> None:
        raise NotImplementedError