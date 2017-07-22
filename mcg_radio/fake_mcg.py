import json

class FakeDisplayController:
    def __init__(self):
        pass

    def setup(self):
        pass

    def set_message(self, message):
        print("Message: %s"% (message))

    def set_title(self, title):
        print("Title: %s" % (title))


class FakeNuttonsListener:
    def __init__(self, pin_previous=26, pin_next=19, debounce=0.1):
        pass

    def setup(self, playback_controller):
        pass


class FakePlaybackController:
    def __init__(self, display_controller):
        pass

    def update_radios(self, radios_json):
        with open(radios_json) as f:
            self.radios = json.load(f)

    def play(self, index=None):
        pass

    def stop(self):
        pass

    def next(self):
        pass

    def previous(self):
        pass