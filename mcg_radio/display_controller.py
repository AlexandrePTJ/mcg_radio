from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1322


class DisplayController:
    def __init__(self):
        self.serial = spi(device=0, port=0)
        self.device = ssd1322(self.serial, 256, 64, 2, "1", "diff_to_previous")

    def setup(self):
        self.device.clear()
        with canvas(self.device) as draw:
            draw.rectangle(self.device.bounding_box, outline="black", fill="white")

    def set_message(self, message):
        pass
