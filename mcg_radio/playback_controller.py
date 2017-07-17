import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject


class PlaybackController:

    def __init__(self, display_controller):
        Gst.init(None)
        self.radios = dict()

        self.player = Gst.ElementFactory.make('playbin', 'player')
        bus = self.player.get_bus()
        bus.enable_sync_message_emission()
        bus.add_signal_watch()
        bus.connect('message::tag', self._on_message)

    def _on_message(self, bus, message):
        taglist = message.parse_tag()
        for x in range(taglist.n_tags()):
            name = taglist.nth_tag_name(x)
            if name == 'title':
                print('%s' % (taglist.get_string(name)[1]))

    def update_radios(self, radios):
        self.radios = radios

    def play(self, index=None):
        if index is None:
            return
        if index in self.radios:
            self.player.set_property('uri', self.radios[index]['url'])
            self.player.set_state(Gst.State.PLAYING)

    def stop(self):
        self.player.set_state(Gst.State.NULL)

    def next(self):
        print('next')

    def previous(self):
        print('previous')
