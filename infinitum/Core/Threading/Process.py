from typing import Callable, Dict, Tuple, Optional
import multiprocessing

class Process:
    def __init__(self, function: Callable, *args: Optional[Tuple], **kwargs: Optional[Dict]) -> None:
        self.__queue, self.__exit = multiprocessing.Queue(), multiprocessing.Queue(1)
        self.__function, self.__args, self.__kwargs = function, args, kwargs
        self.__kwargs['_queue'], self.__kwargs['_EXIT'] = self.__queue, self.__exit
        self.__process = multiprocessing.Process(target = function, args = args, kwargs = kwargs)
        self.__started = False
        
    def start(self):
        self.__process.start()
        self.__process.join()
        self.__started = True

    def is_alive(self):
        return self.__process.exitcode not in (0, None)

    def is_started(self):
        return self.__started

if __name__ == '__main__':
    pass