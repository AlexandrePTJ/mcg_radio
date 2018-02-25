# coding: utf-8

from queue import Queue
from http.server import BaseHTTPRequestHandler, HTTPServer
import re

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
            res = re.match("^/play\?(pos|id)=(\d+)$", self.path)
            if res is None:
                self.send_error(404)

            val = int(res.group(2))
            if res.group(1) == "pos":
                station = dba.get_station_by_position(val)
            else:
                station = dba.get_station_by_id(val)
            m.play(station)

            self.send_response(200)

    httpd = HTTPServer(('', 5000), PlayStationHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
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
