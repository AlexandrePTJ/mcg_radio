# coding: utf-8

import cherrypy


class RestApp(object):

    def __init__(self, mpdcontroller, dba):
        self._mpdctrl = mpdcontroller
        self._dba = dba

    @cherrypy.expose
    def play(self, pos=-1, id=-1):
        if int(pos) > -1:
            station = self._dba.get_station_by_position(pos)
            self._mpdctrl.play(station)
        elif int(station) > -1:
            station = self._dba.get_station_by_id(id)
            self._mpdctrl.play(station)
