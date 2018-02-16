from queue import Queue
from mpdcontroller import MPDController
from displaycontroller import DisplayController
from flask import Flask
from apiproxy import initialize_api


def main():
    q = Queue()

    d = DisplayController(q)
    d.start()

    m = MPDController(q)
    m.reload()
    m.connect()
    m.start()

    app = Flask(__name__)
    initialize_api(app, mpd_controller=m)
    app.run(debug=True, threaded=True)

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
