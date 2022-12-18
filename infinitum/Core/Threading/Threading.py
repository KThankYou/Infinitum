from Infinitum.Core.Threading import Process, Pipes, Queue

class ThreadHandler:
    def __init__(self) -> None:
        self.__sudo, self.__sudo_pid = {0: 'Reserved'}, 0
        self.__children, self.__pid = {10000: 'Reserved'}, 10000
        self.__pipes, self.__queues = [], []

    def isalive(self, pid: int) -> bool:
        raise NotImplementedError

    def create_process(self, function: Callable, args: Optional[Tuple] = None, kwargs: Optional[Dict] = None, sudo: bool = False) -> Process:
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