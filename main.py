from queue import Queue
from mpdcontroller import MPDController
from displaycontroller import DisplayController
from flask import Flask
from apiproxy import initialize_api


def main():
    try:
        q = Queue()

        d = DisplayController(q)
        d.start()

        m = MPDController(q)
        m.reload()
        m.connect()
        m.start()

        app = Flask(__name__)
        initialize_api(app, mpd_controller=m)
        app.run()

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
