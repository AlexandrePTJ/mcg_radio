from mpd import MPDClient
from threading import Thread


class MPDController(Thread):

    _q = None              # Message queue
    _forever = False       # thread loop
    _client = MPDClient()  # MPD client
    _playlist = {}         # Indexed playlist

    def __init__(self, q):
        Thread.__init__(self)
        self._q = q

    def connect(self, host='localhost', port=6600):
        self._client.connect(host, port)

    def run(self):
        self._forever = True
        while self._forever:
            status = self._client.status()
            if status['state'] != 'play':
                self._q.put({'station': 'None'})
            elif 'songid' in status:
                playid = self._client.playlistid(status['songid'])
                if len(playid) == 1:
                    msg = {}
                    for k in ['title', 'name']:
                        if k in playid[0]:
                            msg[k] = playid[0][k]
                    self._q.put(msg)
            self._client.idle()

    def stop(self):
        self._forever = False
        self._client._write_command("noidle")

    def play(self, id):
        if id in self._playlist:
            self._q.put({'station': self._playlist[id]})

    def setup(self, playlist):
        self._playlist = playlist
