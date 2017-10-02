import time
from queue import Queue
from mpdcontroller import MPDController
from displaycontroller import DisplayController
from flask import Flask
from flask_restful import Api
from apiproxy import *


def main():
    try:
        q = Queue()

        d = DisplayController(q)
        d.start()

        m = MPDController(q)
        m.connect()
        m.start()

        app = Flask(__name__)
        api = Api(app)
        api.add_resource(Infos, '/infos', resource_class_kwargs={'mpd_controller': m})
        app.run()

        #while True:
        #    time.sleep(1)

    except (KeyboardInterrupt, SystemExit):
        m.stop()
        d.stop()
        # will unlock DisplayController
        q.put('quit')

    finally:
        m.join(5)
        d.join(5)


if __name__ == '__main__':
    main()