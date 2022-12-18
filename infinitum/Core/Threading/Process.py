from typing import Callable, Dict, Tuple, Optional
import multiprocessing

class Process:
    def __init__(self, function: Callable, args: Optional[Tuple] = None, kwargs: Optional[Dict] = None) -> None:
        self.__queue, self.__exit = multiprocessing.Queue(), multiprocessing.Queue(1)
        self.__function, self.__args, self.__kwargs = function, args, kwargs
        self.__kwargs['_queue'], self.__kwargs['_EXIT'] = self.__queue, self.__exit
        self.__process = multiprocessing.Process(target = function, args = args, kwargs = kwargs)
        self.__started = False

    def restart(self):
        self.terminate()
        self.__process.join()
        while not self.__queue.empty(): self.__queue.get()
        self.__process = multiprocessing.Process(target = self.__function, args = self.__args, kwargs = self.__kwargs)
        self.start()
        
    def start(self):
        try:
            self.__process.start()
            self.__started = True
        except multiprocessing.ProcessError:
            pass #TODO API HANDLER exception

    def terminate(self, force = False):
        self.__queue.cancel_join_thread()
        self.__exit.put(1)
        if force: self.__process.terminate()

    def is_alive(self):
        return self.__process.exitcode not in (0, None)

    def is_started(self):
        return self.__started

    def __iter__(self):
        while True:
            try: yield self.__queue.get(timeout = 2)
            except: break

if __name__ == '__main__':
    pass