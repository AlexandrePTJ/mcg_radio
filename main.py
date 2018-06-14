# coding: utf-8

import cherrypy
from queue import Queue

from buttonslistener import ButtonsListener
from dbaccess import DBAccess
from displaycontroller import DisplayController
from mpdcontroller import MPDController
from restapp import RestApp


def main():
    dba = DBAccess("../mcg_radio.db")
    q = Queue()

    d = DisplayController(q)
    d.start()

    m = MPDController(q, dba)
    m.connect()
    m.start()

    bl = ButtonsListener()
    bl.setup(m, dba)

    try:
        cherrypy.config.update({'engine.autoreload.on': True})
        cherrypy.config.update({'server.socket_port': 5000})
        cherrypy.quickstart(RestApp(m, dba))
    except KeyboardInterrupt:
        pass

    m.stop()
    d.stop()
    # will unlock DisplayController
    q.put('quit')

    m.join()
    print("MPDController joined")
    d.join()
    print("DisplayController joined")


if __name__ == '__main__':
    main()
