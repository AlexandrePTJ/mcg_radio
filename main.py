import gbulb
from aiohttp import web

from mcg_radio.fake_mcg import FakeDisplayController as DisplayController
from mcg_radio.fake_mcg import FakeButtonsListener as ButtonsListener
from mcg_radio.playback_controller import PlaybackController
from mcg_radio.webapp import make_webapp
from mcg_radio import Settings


def main():
    settings = Settings()
    settings.read()

    # Display
    dc = DisplayController()
    dc.setup()

    # Playback
    pc = PlaybackController(settings, dc)

    # User interface
    btl = ButtonsListener()
    btl.setup(pc)

    # WebApp is used as loop.run_forever() bridge
    web.run_app(make_webapp(settings), host='127.0.0.1', port=8080)


if __name__ == '__main__':
    # GLib and asyncio
    gbulb.install()
    # Application
    main()
