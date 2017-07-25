from gpiozero import Button


class ButtonsListener:
    def __init__(self, pin_previous=26, pin_next=19, debounce=0.1):
        self.btPrev = Button(pin_previous, True, debounce)
        self.btNext = Button(pin_next, True, debounce)

    def setup(self, playback_controller):
        self.btPrev.when_pressed = playback_controller.previous
        self.btNext.when_pressed = playback_controller.next
