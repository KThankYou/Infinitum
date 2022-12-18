from multiprocessing import Queue

class DesktopWindowManager:
    def __init__(self) -> None:
        print('dwm started')

def init(_queue: Queue, _EXIT: Queue, **kwargs):
    global queue, EXIT, dwm
    queue, EXIT = _queue, _EXIT
    dwm = DesktopWindowManager()
    main()

def main():
    # i is for testing purposes
    i = 1
    while i < 10:
        if not EXIT.empty(): break
        queue.put(i)
        i += 1