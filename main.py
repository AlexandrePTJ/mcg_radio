import asyncio
import json
import signal

#from mcg_radio.display_controller import DisplayController
#from mcg_radio.buttons_listener import ButtonsListener
from mcg_radio.playback_controller import PlaybackController


class McgRadio:

    def __init__(self):
        pass

    def load_radios(self, radios_json):
        with open(radios_json) as f:
            self.radios = json.load(f)

    def run(self):
        PlaybackController.start_glib_loop()
        #dc = DisplayController()
        #dc.setup()
        pc = PlaybackController(None)
        pc.update_radios(self.radios)
        pc.play("1")
        #btl = ButtonsListener(pc)

        loop = asyncio.get_event_loop()
        loop.add_signal_handler(
            signal.SIGINT,
            loop.run_until_complete,
            loop.shutdown_asyncgens())

        try:
            loop.run_forever()
        finally:
            loop.close()
            pc.stop()
            PlaybackController.stop_glib_loop()


if __name__ == '__main__':
    mr = McgRadio()
    mr.load_radios('radios.json')
    mr.run()
