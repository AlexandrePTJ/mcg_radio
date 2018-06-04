# coding: utf-8

import os
import cherrypy


class RestApp(object):

    def __init__(self, mpdcontroller, dba):
        self._mpdctrl = mpdcontroller
        self._dba = dba

    @cherrypy.expose
    def play(self, pos=None, id=None, url=None):
        if pos is not None:
            station = self._dba.get_station_by_position(pos)
            self._mpdctrl.play(station)
        elif id is not None:
            station = self._dba.get_station_by_id(id)
            self._mpdctrl.play(station)
        elif url is not None:
            self._mpdctrl.direct_play(url)

    @cherrypy.expose
    def setvolume(self, v):
        self._mpdctrl.set_volume(v)

    @cherrypy.expose
    def shutdown(self):
        os.system("sudo shutdown -h now")
