import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

import threading

class PlaybackController:

    glib_loop = None
    glib_thread = None

    def __init__(self, display_controller):
        self.radios = dict()

        self.player = Gst.ElementFactory.make('playbin', 'player')
        bus = self.player.get_bus()
        bus.enable_sync_message_emission()
        bus.add_signal_watch()
        bus.connect('message::tag', self._on_message)

    @classmethod
    def start_glib_loop(cls):
        GObject.threads_init()
        Gst.init(None)
        cls.glib_loop = GObject.MainLoop()
        cls.glib_thread = threading.Thread(target=cls.glib_loop.run)
        cls.glib_thread.start()

    @classmethod
    def stop_glib_loop(cls):
        cls.glib_loop.quit()
        cls.glib_thread.join()
        cls.glib_loop = cls.glib_thread = None

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
