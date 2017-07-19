from aiohttp import web


async def index(request):
    request.app['PlaybackController'].next()
    return web.Response(text='Hello Aiohttp!')
