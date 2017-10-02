from flask_restful import Resource


class RestMpdProxyResource(Resource):
    def __init__(self, **kwargs):
        self._mpdcontroller = kwargs['mpd_controller']


class Infos(RestMpdProxyResource):
    def __init__(self, **kwargs):
        super(Infos, self).__init__(**kwargs)

    def get(self):
        return self._mpdcontroller.infos()
