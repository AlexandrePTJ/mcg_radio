from flask_restful import Api, Resource


class RestMpdProxyResource(Resource):
    def __init__(self, **kwargs):
        self._mpdcontroller = kwargs['mpd_controller']


class Infos(RestMpdProxyResource):
    def __init__(self, **kwargs):
        super(Infos, self).__init__(**kwargs)

    def get(self):
        return self._mpdcontroller.infos()


class Playlist(RestMpdProxyResource):
    def __init__(self, **kwargs):
        super(Playlist, self).__init__(**kwargs)

    def get(self):
        return self._mpdcontroller.playlist()


class Next(RestMpdProxyResource):
    def __init__(self, **kwargs):
        super(Next, self).__init__(**kwargs)

    def get(self):
        return self._mpdcontroller.next()


class Previous(RestMpdProxyResource):
    def __init__(self, **kwargs):
        super(Previous, self).__init__(**kwargs)

    def get(self):
        return self._mpdcontroller.previous()


def initialize_api(app, mpd_controller):
    kw = {'mpd_controller': mpd_controller}
    api = Api(app)
    api.add_resource(Infos, '/infos', resource_class_kwargs=kw)
    api.add_resource(Playlist, '/playlist', resource_class_kwargs=kw)
    api.add_resource(Next, '/next', resource_class_kwargs=kw)
    api.add_resource(Previous, '/previous', resource_class_kwargs=kw)
