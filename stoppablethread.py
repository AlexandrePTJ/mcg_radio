from threading import Event, Thread


class StoppableThread(Thread):
    _stopper = Event()

    def __init__(self):
        super(StoppableThread, self).__init__()

    def stop(self):
        self._stopper.set()

    def stopped(self):
        self._stopper.is_set()
