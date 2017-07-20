from aiohttp import web
import aiohttp_jinja2
import jinja2


class RadiosView(web.View):
	
	@aiohttp_jinja2.template('radios.html')
	async def get(self):
		return { 'radios': self.request.app['PlaybackController'].radios }

	async def post(self):
		pass


def make_webapp(playback_controller):
	app = web.Application()
	aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
	app.router.add_static('/static', 'static')
	app.router.add_route('*', '/', RadiosView)
	app['PlaybackController'] = playback_controller
	return app
