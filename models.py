import logging
import time
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
        self.highest_detected_chance: float = 0.0  # temp variable
        self.key_detected_chance_threshold: float = key_detected_chance_threshold

        self._detected_points: set = set()
        self._detected_changes: List = []
        self._last_match_time = 0
        self._cooldown_time = Config.preview_frame_rate * 0.1
        self._detect_using_points = False

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

        # Detect points in contour
        for point in self.points:
            result = cv2.pointPolygonTest(contour, point, False)
            if result < 1:
                continue

            self.detected_chance += 1 / len(self.points)
            self._detected_points.add(point)

        if self._detect_using_points:
            # Reset if there aren't any points in the contour
            if self.detected_chance == 0.0:
                if self._last_match_time + self._cooldown_time < time.time():
                    self._detected_points.clear()
            else:
                self._last_match_time = time.time()

            # Determine if there are enough points in the contour for a key press
            if len(self._detected_points) > 0.95 * len(self.points):
                self.is_pressed = True
            else:
                self.is_pressed = False

            # temp
            self.highest_detected_chance = len(self._detected_points)
            self.detected_chance = len(self.points)
        else:
            self._detected_changes.append(self.detected_chance)

            # Reset if there aren't any points in the contour
            if self.detected_chance == 0.0:
                if self._last_match_time + self._cooldown_time < time.time():
                    self._detected_changes.clear()
            else:
                self._last_match_time = time.time()

            # Determine if there are enough points in the contour for a key press
            if len(self._detected_changes) == 0:
                detected_average = 0
            else:
                detected_average = sum(self._detected_changes) / len(self._detected_changes)

            if detected_average > 0.3:
                self.is_pressed = True
            else:
                self.is_pressed = False

            # temp
            if detected_average > self.highest_detected_chance:
                self.highest_detected_chance = detected_average

    def __repr__(self):
        return "Key(name={},x={},y={},pressed={})".format(self.name, self.x, self.y, self.is_pressed)
