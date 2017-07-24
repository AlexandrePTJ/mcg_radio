from aiohttp import web

from mcg_radio.fake_mcg import FakeDisplayController as DisplayController
from mcg_radio.fake_mcg import FakePlaybackController as PlaybackController
from mcg_radio.webapp import make_webapp

dc = DisplayController()
dc.setup()

pc = PlaybackController(dc)
pc.update_radios('mcg_radios.json')

# WebApp is used as loop.run_forever() bridge
web.run_app(make_webapp(pc), host='127.0.0.1', port=8080)
