import logging
import os
from typing import Optional

import cv2

from profiles import Profile
from profiles import profiles

logger = logging.getLogger(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    log_level = "INFO"

    profile_name: str = ""
    profile: Optional[Profile] = None

    default_file_name: str = ""
    file_name: str = ""
    gray_scale: bool = True
    is_image: bool = False
    record_output: bool = False
    show_preview_video: bool = False
    preview_frame_rate = 1

    # CALIBRATION
    calibration: bool = False
    minimal_contour_area: int = 50
    calibration_delay_between_keys: float = 0.0
    calibration_key_start_delay: float = 0.0
    calibration_key_stop_delay: float = 0.11
    paint_key_points_as_line: bool = False

    key_points_filter_standard_deviation = [15, 15]

    # PROCESSING
    brightness_threshold: int = 0
    key_brightness_area_size: int = 2
    contour_brightness_threshold: int = 80

    zone_bounds = [
        [100, 249],
        [1920, 705],
    ]

    # PAINTING
    line_width: int = 2
    pressed_color = (255, 255, 255)
    not_pressed_color = (0, 0, 0)
    font_family = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.3
    font_color = (255, 255, 0)
    font_thickness = 2
    line_type = cv2.LINE_AA

    @staticmethod
    def load_profile(profile_name: str = None):
        if profile_name is None:
            profile_name = Config.profile_name

        profile = next(p for p in profiles if p.name == profile_name)
        if profile is None:
            logger.info("Profile not found")
            return

        Config.profile_name = profile_name
        Config.profile = profile
        Config.brightness_threshold = profile.brightness_threshold
        if profile.default_file_name is not None:
            Config.default_file_name = profile.default_file_name

        Config.zone_bounds = profile.zone_bounds
        Config.minimal_contour_area = profile.minimal_contour_area
        Config.calibration_delay_between_keys = profile.calibration_delay_between_keys
        Config.calibration_key_start_delay = profile.calibration_key_start_delay
        Config.calibration_key_stop_delay = profile.calibration_key_stop_delay
        Config.key_points_filter_standard_deviation = profile.key_points_filter_standard_deviation
        Config.contour_brightness_threshold = profile.contour_brightness_threshold
