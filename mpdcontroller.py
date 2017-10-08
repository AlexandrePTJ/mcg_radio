import json
import os.path
from mpd import MPDClient
from stoppablethread import StoppableThread
import time
from threading import Event


class MPDController(StoppableThread):

    _q = None              # Message queue
    _client = MPDClient()  # MPD client
    _playlist = {}         # Indexed playlist
    _infos = {             # Live information
        'title': '',
        'name': '',
        'station': '',
        'id': ''
    }
    _current_station_id = '1'
    _conf_dir = '/home/alexandre/devel/mcg/backend'
    _mpdbusy = Event()     # Do no go idle while sending other cmds

    def __init__(self, q):
        StoppableThread.__init__(self)
        self._q = q

    def connect(self, host='localhost', port=6600):
        self._client.connect(host, port)

    def reload(self):
        # playlist
        if os.path.exists(self._conf_dir + '/playlist.json'):
            with open(self._conf_dir + '/playlist.json') as f:
                self._playlist = json.load(f)

        # current station
        if os.path.exists(self._conf_dir + '/current'):
            pass

        # Fix if id is not here anymore
        if self._current_station_id not in self._playlist:
            self._current_station_id = '1'


    def run(self):
        # Get station to play and send it to mpd
        self.play(self._current_station_id)

        # Looping
        while not self.stopped():
            status = self._client.status()
            if status['state'] != 'play':
                self._infos['station'] = 'None'
                self._q.put(self._infos)
            elif 'songid' in status:
                playid = self._client.playlistid(status['songid'])
                if len(playid) == 1:
                    for k in ['title', 'name']:
                        if k in playid[0]:
                            self._infos[k] = playid[0][k]
                    self._q.put(self._infos)
            self._client.idle()

            # Occurs when 'play' called
            while self._mpdbusy.is_set():
                time.sleep(1)

    def stop(self):
        self._stopper.set()
        self._client._write_command("noidle")

    def play(self, id):
        if id in self._playlist:
            station = self._playlist[id]

            self._current_station_id = id
            self._infos['id'] = id
            self._infos['station'] = station['label']
            self._infos['title'] = ''
            self._infos['name'] = ''

            self._mpdbusy.set()
            self._client._write_command("noidle")
            self._client.clear()
            self._client.add(station['url'])
            self._client.play()
            self._mpdbusy.clear()

    def next(self):
        cidx = int(self._current_station_id)
        next_found = False
        while not next_found and cidx < 100:
            cidx = cidx + 1
            if str(cidx) in self._playlist:
                next_found = True
        if next_found:
            self.play(str(cidx))

    def previous(self):
        cidx = int(self._current_station_id)
        previous_found = False
        while not previous_found and cidx > 0:
            cidx = cidx - 1
            if str(cidx) in self._playlist:
                previous_found = True
        if previous_found:
            self.play(str(cidx))

    def set_playlist(self, playlist):
        self._playlist = playlist

    def playlist(self):
        return self._playlist

    def infos(self):
        return self._infos
