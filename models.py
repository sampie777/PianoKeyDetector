import logging
from typing import List

import cv2

import calibration
from config import Config
import numpy as np

logger = logging.getLogger(__name__)


class Key:
    def __init__(self, name: str,
                 x: int = -1, y: int = -1,
                 points: List = None,
                 color: tuple = (255, 255, 0),
                 is_calibrated: bool = False,
                 key_detected_chance_threshold: float = 0.0):
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.is_pressed: bool = False
        self.color: tuple = color
        self.is_calibrated: bool = is_calibrated
        self.points: List = points if points is not None else []
        self.detected_chance: float = 0.0
        self.highest_detected_chance: float = 0.0   # temp variable
        self.key_detected_chance_threshold: float = key_detected_chance_threshold

    def is_pressed_in_frame(self, frame):
        frame_height, frame_width = frame.shape[:2]

        if self.y < 0 or self.y > frame_height:
            self.is_pressed = False
            return
        if self.x < 0 or self.x > frame_width:
            self.is_pressed = False
            return

        y0 = max(0, min(frame_height - 1, self.y - Config.key_brightness_area_size))
        y1 = max(0, min(frame_height - 1, self.y + Config.key_brightness_area_size))
        x0 = max(0, min(frame_width - 1, self.x - Config.key_brightness_area_size))
        x1 = max(0, min(frame_width - 1, self.x + Config.key_brightness_area_size))
        test_area = frame[y0:y1, x0:x1]

        average_brightness = np.sum(test_area) / ((y1 - y0) * (x1 - x0))

        logger.debug("{}: {}".format(self, average_brightness))
        self.is_pressed = average_brightness > Config.brightness_threshold

    def check_for_contour(self, contour):
        self.detected_chance = 0.0

        for point in self.points:
            result = cv2.pointPolygonTest(contour, point, False)
            if result < 1:
                continue

            self.detected_chance += 1 / len(self.points)

        if self.detected_chance > self.key_detected_chance_threshold:
            self.is_pressed = True
        else:
            self.is_pressed = False

        # temp
        if self.detected_chance > self.highest_detected_chance:
            self.highest_detected_chance = self.detected_chance

    def __repr__(self):
        return "Key(name={},x={},y={},pressed={})".format(self.name, self.x, self.y, self.is_pressed)
