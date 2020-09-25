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

    # PROCESSING
    minimal_contour_area: int = 50
    contour_brightness_threshold: int = 80

    zone_bounds = [
        [100, 249],
        [1920, 705],
    ]

    # CALIBRATION
    calibrating: bool = False
    key_amount_to_calibrate: int = 30

    calibration_delay_between_keys: float = 0.0
    calibration_key_start_delay: float = 0.0
    calibration_key_stop_delay: float = 0.11
    key_points_filter_standard_deviation = [15, 15]

    # OUTPUT
    save_to_midi: bool = True
    midi_min_note_duration: float = 1/8
    midi_track_name: str = "Detected Track"
    midi_track_index: int = 0
    midi_channel: int = 0
    midi_tempo: int = 120
    midi_volume: int = 100
    midi_pitch_offset_octave: int = 3

    save_to_video: bool = True
    output_video_file_name: str = "/home/prive/IdeaProjects/PianoKeyDetector/output.mp4"
    output_video_codec: str = "MP4V"

    show_preview_video: bool = False
    preview_frame_rate = 1

    # PAINTING
    line_type = cv2.LINE_AA
    font_family = cv2.FONT_HERSHEY_SIMPLEX
    key_dot_radius: int = 4
    key_dot_thickness: int = 2
    key_dot_pressed_color = (255, 255, 255)
    key_dot_not_pressed_color = (0, 0, 0)
    key_name_font_scale = 1.3
    key_name_font_thickness = 2
    key_line_thickness = 2
    key_point_radius = 1
    key_point_thickness = -1
    text_distance_to_key: int = 10

    contour_center_radius = 5
    contour_center_thickness = -1

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
        if profile.default_file_name is not None:
            Config.default_file_name = profile.default_file_name

        Config.zone_bounds = profile.zone_bounds
        Config.minimal_contour_area = profile.minimal_contour_area
        Config.calibration_delay_between_keys = profile.calibration_delay_between_keys
        Config.calibration_key_start_delay = profile.calibration_key_start_delay
        Config.calibration_key_stop_delay = profile.calibration_key_stop_delay
        Config.key_points_filter_standard_deviation = profile.key_points_filter_standard_deviation
        Config.contour_brightness_threshold = profile.contour_brightness_threshold
