# coding: utf-8

from mpd import MPDClient
import time
from threading import Event, Thread
import requests


class MPDController(Thread):

    _q = None              # Message queue
    _client = MPDClient()  # MPD client
    _infos = {             # Live information
        'title': '',
        'name': '',
        'position': ''
    }
    _mpdbusy = Event()     # Do no go idle while sending other cmds
    _connected = False
    _stopper = Event()

    def __init__(self, q, dba):
        super(MPDController, self).__init__()
        self._q = q
        self._dba = dba

    def connect(self, host='localhost', port=6600):
        try:
            self._client.connect(host, port)
            self._connected = True
        except ConnectionError as ce:
            pass

    def run(self):
        # Get station to play and send it to mpd
        station = self._dba.get_current_station()
        self.play(station)

        # Looping
        while not self._stopper.is_set():
            if not self._connected:
                time.sleep(1)
                continue

            status = self._client.status()

            if status['state'] != 'play':
                self._q.put({})

            elif 'songid' in status:
                playid = self._client.playlistid(status['songid'])
                if len(playid) == 1:
                    for k in ['title', 'name']:
                        if k in playid[0]:
                            self._infos[k] = playid[0][k]
                    self._dba.update_current_info(
                        self._infos['title'],
                        self._infos['name'])
                    self._q.put(self._infos)

            self._client.idle()

            # Occurs when 'play' called
            while self._mpdbusy.is_set():
                time.sleep(1)

    def stop(self):
        self._stopper.set()
        if self._connected:
            self._client._write_command("noidle")
            self._connected = False

    def play(self, station):
        if station:
            self._dba.clear_current_info()
            self._dba.set_current_station(station)
            self._infos['position'] = str(station['position'])

            stream = self._extract_stream(station['stream_url'])

            if self._connected:
                self._mpdbusy.set()
                self._client._write_command("noidle")
                self._client.clear()
                self._client.add(stream)
                self._client.setvol(station['volume'])
                self._client.play()
                self._mpdbusy.clear()

    def direct_play(self, url):
        if not self._connected:
            return

        self._dba.clear_current_info()
        self._dba.set_current_station({'id': -1})
        self._infos['position'] = "-1"

        stream = self._extract_stream(url)
        self._mpdbusy.set()
        self._client._write_command("noidle")
        self._client.clear()
        self._client.add(stream)
        self._client.setvol(80)
        self._client.play()
        self._mpdbusy.clear()

    def set_volume(self, v):
        if not self._connected:
            return
        self._client.setvol(v)

    ''' Because TuneIn can send .m3u instead of real stream '''
    def _extract_stream(self, dbstream):
        if dbstream.endswith('.m3u'):
            r = requests.get(dbstream, allow_redirects=True)
            for l in r.text.splitlines():
                if not l.startswith("#"):
                    return l
            return ""
        else:
            return dbstream
