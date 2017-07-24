from aiohttp import web
import aiohttp_jinja2
import jinja2


class RadiosView(web.View):

    @aiohttp_jinja2.template('radios.html')
    async def get(self):
        radios = self.request.app['PlaybackController'].radios
        return {'radios': radios}

    async def post(self):
        data = await self.request.post()
        radios_count = int(data['radios_count'])
        radios = []
        for n in range(1, radios_count + 1):
            lbl_n = data['label_' + str(n)]
            url_n = data['url_' + str(n)]
            if lbl_n and url_n:
                radios.append({'label': lbl_n, 'url': url_n, 'index': n})
        self.request.app['PlaybackController'].radios = radios
        return web.HTTPFound('/')


def make_webapp(playback_controller):
    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
    app.router.add_static('/static', 'static')
    app.router.add_route('*', '/', RadiosView)
    app['PlaybackController'] = playback_controller
    return app
