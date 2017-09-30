import time
from queue import Queue
from mpdcontroller import MPDController
from displaycontroller import DisplayController


def main():
    try:
        q = Queue()

        d = DisplayController(q)
        d.start()

        m = MPDController(q)
        m.connect()
        m.start()

        while True:
            time.sleep(1)

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