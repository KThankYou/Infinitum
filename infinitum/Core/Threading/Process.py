import multiprocessing

class Process:
    def __init__(self, function: Callable, args: Optional[Tuple] = None, kwargs: Optional[Dict] = None) -> None:
        