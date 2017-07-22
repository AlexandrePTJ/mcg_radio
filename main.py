import gbulb
from aiohttp import web

from mcg_radio.fake_mcg import FakeDisplayController as DisplayController
#from mcg_radio.buttons_listener import ButtonsListener
from mcg_radio.playback_controller import PlaybackController
from mcg_radio.webapp import make_webapp


def main():
    # Display
    dc = DisplayController()
    dc.setup()

    # Playback
    pc = PlaybackController(dc)
    pc.update_radios('radios.json')

    # User interface
    # btl = ButtonsListener(pc)

    # WebApp is used as loop.run_forever() bridge
    web.run_app(make_webapp(pc), host='127.0.0.1', port=8080)


if __name__ == '__main__':
    # GLib and asyncio
    gbulb.install()
    # Application
    main()
