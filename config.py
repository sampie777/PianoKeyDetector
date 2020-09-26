import logging
import os
from typing import Optional

import cv2
import numpy as np

import project_state
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
    mask_area = np.array([(120, 400),
                          (1690, 270),
                          (1710, 417),
                          (141, 430)])

    # CALIBRATION
    calibrating: bool = False
    calibrate_zone: bool = True
    key_amount_to_calibrate: int = 30

    calibration_delay_between_keys: float = 0.0
    calibration_key_start_delay: float = 0.0
    calibration_key_stop_delay: float = 0.11
    key_points_filter_standard_deviation = [15, 15]

    # OUTPUT
    save_to_midi: bool = True
    midi_min_note_duration: float = 1/8
    midi_round_note_to_beat: bool = True
    midi_track_name: str = "Detected Track"
    midi_track_index: int = 0
    midi_channel: int = 0
    midi_tempo: int = 120
    midi_volume: int = 100
    midi_pitch_offset_octave: int = 3

    save_to_video: bool = True
    output_video_file_name: str = "/home/prive/IdeaProjects/PianoKeyDetector/output.mp4"
    output_video_codec: str = "MP4V"

    show_preview_video: bool = True
    preview_window_title = "Piano Key Detector"
    preview_frame_rate = 1
    display_debug_info: bool = False

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
    paint_key_points_if_line_available: bool = False
    text_distance_to_key: int = 10

    paint_mask_outline: bool = True

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
        Config.mask_area = profile.mask_area
        Config.minimal_contour_area = profile.minimal_contour_area
        Config.calibration_delay_between_keys = profile.calibration_delay_between_keys
        Config.calibration_key_start_delay = profile.calibration_key_start_delay
        Config.calibration_key_stop_delay = profile.calibration_key_stop_delay
        Config.key_points_filter_standard_deviation = profile.key_points_filter_standard_deviation
        Config.contour_brightness_threshold = profile.contour_brightness_threshold

    @staticmethod
    def update_project_state():
        project_state.zone_bounds = Config.zone_bounds
        project_state.mask_area = Config.mask_area
