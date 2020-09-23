import logging

from config import Config
import numpy as np

logger = logging.getLogger(__name__)


class Key:
    def __init__(self, name: str, x: int, y: int):
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.pressed: bool = False

    def is_pressed_in_frame(self, frame):
        frame_height, frame_width = frame.shape[:2]

        if self.y < 0 or self.y > frame_height:
            self.pressed = False
            return
        if self.x < 0 or self.x > frame_width:
            self.pressed = False
            return

        y0 = max(0, min(frame_height - 1, self.y - Config.key_brightness_area_size))
        y1 = max(0, min(frame_height - 1, self.y + Config.key_brightness_area_size))
        x0 = max(0, min(frame_width - 1, self.x - Config.key_brightness_area_size))
        x1 = max(0, min(frame_width - 1, self.x + Config.key_brightness_area_size))
        test_area = frame[y0:y1, x0:x1]

        average_brightness = np.sum(test_area) / ((y1 - y0) * (x1 - x0))

        logger.debug("{}: {}".format(self, average_brightness))
        self.pressed = average_brightness > Config.brightness_threshold

    def __repr__(self):
        return "Key(name={},x={},y={},pressed={})".format(self.name, self.x, self.y, self.pressed)
