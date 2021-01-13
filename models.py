import logging
import time
from typing import List

import cv2
import numpy as np

from config import Config

logger = logging.getLogger(__name__)


class Key:
    note_base_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    def __init__(self, name: str,
                 x: int = -1, y: int = -1,
                 points: List = None,
                 color: tuple = (255, 255, 0),
                 is_calibrated: bool = False,
                 key_detected_chance_threshold: float = 0.0,
                 line: List = None):
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
        self.line: List = line

        self.midi_pitch = Key.get_pitch_for_key(self.name)

        self._detected_points: set = set()
        self._detected_chances: List = []
        self._detect_chance_threshold = 0.1
        self._detect_using_points = False
        self._detect_using_line = True

        self._press_started_time = None
        self._minimum_duration_time = Config.preview_frame_rate * 0.08
        self._last_match_time = 0
        self._cooldown_time = Config.preview_frame_rate * Config.key_cooldown_time

        self._previous_state: bool = False

    def state_changed(self) -> bool:
        return self.is_pressed != self._previous_state

    def set_pressed(self, is_pressed: bool):
        self._previous_state = self.is_pressed
        self.is_pressed = is_pressed

    def get_center_point(self) -> tuple:
        if self.line is not None:
            return tuple(np.mean(self.line, axis=0))
        if len(self.points) > 0:
            return tuple(np.mean(self.points, axis=0))
        return self.x, self.y

    def check_for_contour(self, contour):
        if self._detect_using_line:
            self._check_for_using_lines(contour)
            return

        # Detect points in contour
        for point in self.points:
            result = cv2.pointPolygonTest(contour, point, False)
            if result < 1:
                continue

            self.detected_chance += 1 / len(self.points)
            self._detected_points.add(point)

    def _check_for_using_lines(self, contour):
        if self.line is None:
            return

        start_point = np.array(self.line[0])
        stop_point = np.array(self.line[1])
        points_on_line = np.linspace(start_point, stop_point,
                                     round(np.linalg.norm(start_point - stop_point)))

        for point in points_on_line:
            result = cv2.pointPolygonTest(contour, tuple(point), False)
            if result < 1:
                continue

            self.detected_chance += 1 / len(points_on_line)

    def check_for_contour_finalize(self):
        if self._detect_using_points:
            self._finalize_using_points()
        elif self._detect_using_line:
            self._finalize_using_lines()
        else:
            self._finalize_using_chances()

    def _finalize_using_lines(self):
        if self.line is None:
            return

        self._detected_chances.append(self.detected_chance)

        # Handle start/stop (delays)
        if self.detected_chance > 0:
            self.detected_chance = 0

            ##
            # Handle START smoother delay
            #
            # Check if press already was started
            if self._press_started_time is None:
                self._press_started_time = time.time()
                self.set_pressed(False)
                return

            # Check if press has started long enough ago
            elif self._press_started_time + self._minimum_duration_time > time.time():
                self.set_pressed(False)
                return

            ##
            # Handle STOP smoother delay
            self._last_match_time = time.time()
        else:
            # If press stopped long enough ago
            if self._last_match_time + self._cooldown_time < time.time():
                self._press_started_time = None
                self._detected_chances.clear()

        # Calculate average detected chance
        if len(self._detected_chances) == 0:
            detected_average = 0
        else:
            detected_average = sum(self._detected_chances) / len(self._detected_chances)

        # The final logic to determine if the detected chance is enough to mark is as a key press
        if detected_average > self._detect_chance_threshold:
            self.set_pressed(True)
        else:
            self.set_pressed(False)

        # temp
        if detected_average > self.highest_detected_chance:
            self.highest_detected_chance = detected_average

    def _finalize_using_chances(self):
        self._detected_chances.append(self.detected_chance)
        # Reset if there aren't any points in the contour
        if self.detected_chance == 0.0:
            if self._last_match_time + self._cooldown_time < time.time():
                self._detected_chances.clear()
        else:
            self._last_match_time = time.time()
        # Determine if there are enough points in the contour for a key press
        if len(self._detected_chances) == 0:
            detected_average = 0
        else:
            detected_average = sum(self._detected_chances) / len(self._detected_chances)
        if detected_average > 0.3:
            self.set_pressed(True)
        else:
            self.set_pressed(False)
        # temp
        if detected_average > self.highest_detected_chance:
            self.highest_detected_chance = detected_average

        self.detected_chance = 0

    def _finalize_using_points(self):
        # Reset if there aren't any points in the contour
        if self.detected_chance == 0.0:
            if self._last_match_time + self._cooldown_time < time.time():
                self._detected_points.clear()
        else:
            self._last_match_time = time.time()
        # Determine if there are enough points in the contour for a key press
        if len(self._detected_points) > 0.92 * len(self.points):
            self.set_pressed(True)
        else:
            self.set_pressed(False)
        # temp
        self.highest_detected_chance = len(self._detected_points)
        self.detected_chance = len(self.points)

    def __repr__(self):
        return "Key(name={},is_pressed={},is_calibrated={})".format(self.name, self.is_pressed, self.is_calibrated)

    @staticmethod
    def get_pitch_for_key(key_name: str) -> int:
        octave = int(key_name[-1:]) + Config.midi_pitch_offset_octave
        note = key_name[:-1]

        index = Key.note_base_names.index(note)

        pitch = 12 + index + 12 * octave
        logger.info("Pitch for key '{}' is: {}".format(key_name, pitch))
        return pitch
