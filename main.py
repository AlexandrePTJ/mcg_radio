import asyncio
import functools
import os
import signal

from mcg_radio.playback_controller import PlaybackController
from mcg_radio.buttons_listener import ButtonsListener


class McgRadio:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        for sign in ('SIGINT', 'SIGTERM'):
            self.loop.add_signal_handler(getattr(signal, sign),
                                         functools.partial(self.ask_exit, sign))

    def ask_exit(self, signame):
        print("got signal %s: exit" % signame)
        self.loop.stop()

    def run(self):
        pc = PlaybackController()
        btl = ButtonsListener(pc)

        try:
            print("Event loop running forever, press Ctrl+C to interrupt.")
            print("pid %s: send SIGINT or SIGTERM to exit." % os.getpid())
            self.loop.run_forever()
        finally:
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.close()


if __name__ == '__main__':
    mr = McgRadio()
    mr.run()
