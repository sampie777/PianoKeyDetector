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
    calibration: bool = False
    preview_frame_rate = 1

    # PROCESSING
    brightness_threshold: int = 0
    key_brightness_area_size = 5

    line_width: int = 2
    pressed_color = (255, 255, 255)
    not_pressed_color = (0, 0, 0)
    text_font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
    font_color = (255, 255, 0)
    font_thickness = 5
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
