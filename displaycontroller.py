from stoppablethread import StoppableThread


class DisplayController(StoppableThread):

    _q = None         # Message queue

    def __init__(self, q):
        StoppableThread.__init__(self)
        self._q = q

    def run(self):
        while not self.stopped():
            message = self._q.get()
            if isinstance(message, dict):
                self._process_dict_message(message)
            elif isinstance(message, str):
                self._process_string_message(str)

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
