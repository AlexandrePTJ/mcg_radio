from gpiozero import Button


class ButtonsListener:
    def __init__(self, playback_controller, pin_previous=26, pin_next=19, debounce=0.1):
        # Previous
        self.btPrev = Button(pin_previous, True, debounce)
        self.btPrev.when_pressed = playback_controller.previous

        # Next
        self.btNext = Button(pin_next, True, debounce)
        self.btNext.when_pressed = playback_controller.next
