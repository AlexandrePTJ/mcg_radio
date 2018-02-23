#coding: utf-8

from queue import Queue
from http.server import BaseHTTPRequestHandler, HTTPServer

from mpdcontroller import MPDController
from displaycontroller import DisplayController
from dbaccess import DBAccess


def main():
    dba = DBAccess("../mcg_radio.db")
    q = Queue()

    d = DisplayController(q)
    d.start()

    m = MPDController(q, dba)
    m.connect()
    m.start()

    class PlayStationHandler(BaseHTTPRequestHandler):

        def do_GET(self):
            if self.path == '/play':
                self.send_response(200)
            else:
                self.send_error(404)

    httpd = HTTPServer(('', 5000), PlayStationHandler)
    httpd.serve_forever()

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
