# coding: utf-8

from threading import Event, Thread


class DisplayController(Thread):

    _q = None         # Message queue
    _stopper = Event()

    def __init__(self, q):
        super(DisplayController, self).__init__()
        self._q = q

    def run(self):
        while not self._stopper.is_set():
            message = self._q.get()
            if isinstance(message, dict):
                self._process_dict_message(message)
            elif isinstance(message, str):
                self._process_string_message(str)

    def stop(self):
        self._stopper.set()

    def _process_string_message(self, msg):
        if msg == 'quit':
            print('Good Bye !')

    # may contains title, name and station keys
    def _process_dict_message(self, msg):
        if 'title' in msg:
            print('Playing : %s' % msg['title'])
        if 'name' in msg:
            print('Message : %s' % msg['name'])
        if 'station' in msg:
            print('Station : %s' % msg['station'])
        if 'id' in msg:
            print('ID : %s' % msg['id'])
