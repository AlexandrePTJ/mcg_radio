# Be able to create a fake button class for dev
try:
    from gpiozero import Button
except ImportError:
    class Button(object):
        def __init__(self, pin=0, pull_up=True, hold_time=0, bounce_time=0.0):
            super(Button, self).__init__()


from subprocess import check_call
from functools import partial


class ButtonsListener:

    def __init__(self, pin_previous=23, pin_next=22, pin_1=4, pin_2=22, pin_3=26 , pin_4=17 , pin_5=5 , pin_6=14 , pin_7=27 , pin_8=13 , pin_9=15, pin_off=16, debounce=0.1):
        #self.btPrev = Button(pin_previous, True, debounce)
        #self.btNext = Button(pin_next, True, debounce)
        self.bt_1 = Button(pin_1, True, debounce)
        self.bt_2 = Button(pin_2, True, debounce)
        self.bt_3 = Button(pin_3, True, debounce)
        self.bt_4 = Button(pin_4, True, debounce)
        self.bt_5 = Button(pin_5, True, debounce)
        self.bt_6 = Button(pin_6, True, debounce)
        self.bt_7 = Button(pin_7, True, debounce)
        self.bt_8 = Button(pin_8, True, debounce)
        self.bt_9 = Button(pin_9, True, debounce)
        self.bt_off = Button(pin=pin_off, pull_up=True, hold_time=2, bounce_time=debounce)

    def setup(self, mpdcontroller, dba):
        self._mpdcontroller = mpdcontroller
        self._dba = dba
        #self.btPrev.when_pressed = playback_controller.previous
        #self.btNext.when_pressed = playback_controller.next
        self.bt_1.when_pressed = partial(self._play, pos=1)
        self.bt_2.when_pressed = partial(self._play, pos=2)
        self.bt_3.when_pressed = partial(self._play, pos=3)
        self.bt_4.when_pressed = partial(self._play, pos=4)
        self.bt_5.when_pressed = partial(self._play, pos=5)
        self.bt_6.when_pressed = partial(self._play, pos=6)
        self.bt_7.when_pressed = partial(self._play, pos=7)
        self.bt_8.when_pressed = partial(self._play, pos=8)
        self.bt_9.when_pressed = partial(self._play, pos=9)
        self.bt_off.when_pressed = self._shutdown

    def _shutdown(self):
        check_call(['sudo', 'poweroff'])

    def _play(self, pos=0):
        station = self._dba.get_station_by_position(pos)
        self._mpdcontroller.play(station)
