from typing import List, Optional

import numpy as np


class Profile:
    def __init__(self, name: str,
                 start_location: tuple = (0, 0),
                 x_increment: float = 0,
                 y_increment: float = 0,
                 a: float = 1,
                 b: float = 1,
                 c: float = 1,
                 brightness_threshold: int = 0,
                 skip_to_time: float = 0,
                 default_file_name: Optional[str] = None,
                 zone_bounds: Optional[List] = None,
                 mask_area: np.ndarray = None,
                 minimal_contour_area: int = 0,
                 calibration_delay_between_keys: float = 0,
                 calibration_key_start_delay: float = 0,
                 calibration_key_stop_delay: float = 0,
                 key_points_filter_standard_deviation: List = None,
                 contour_brightness_threshold: int = 0,
                 key_amount_to_calibrate: int = 30,
                 ):
        self.key_amount_to_calibrate = key_amount_to_calibrate
        self.name = name
        self.start_location = start_location
        self.x_increment = x_increment
        self.y_increment = y_increment
        self.a = a
        self.b = b
        self.c = c
        self.brightness_threshold = brightness_threshold
        self.default_file_name = default_file_name

        self.skip_to_time = skip_to_time

        self.zone_bounds: Optional[List] = zone_bounds
        self.mask_area: Optional[np.ndarray] = mask_area
        self.minimal_contour_area = minimal_contour_area
        self.calibration_delay_between_keys = calibration_delay_between_keys
        self.calibration_key_start_delay = calibration_key_start_delay
        self.calibration_key_stop_delay = calibration_key_stop_delay
        self.key_points_filter_standard_deviation = key_points_filter_standard_deviation \
            if key_points_filter_standard_deviation is not None else [0, 0]
        self.contour_brightness_threshold = contour_brightness_threshold


def get_average_brightness_for(min: int, max: int) -> int:
    return min + (max - min) // 2


profiles: List[Profile] = [
    Profile("IMG_20200922_170508.jpg 1.0",  # 0
            start_location=(1390, 1571),
            x_increment=7,
            y_increment=35,
            a=1.002,
            b=1.0005,
            c=1.00005,
            brightness_threshold=get_average_brightness_for(412, 489),
            default_file_name="/home/prive/IdeaProjects/PianoKeyDetector/resources/IMG_20200922_170508.jpg"
            ),
    Profile("IMG_20200922_170508.jpg 2.0",  # 1
            start_location=(1550, 1571),
            x_increment=13,
            y_increment=42,
            a=1.002,
            b=1.0005,
            c=1.00005,
            brightness_threshold=get_average_brightness_for(412, 489),
            default_file_name="/home/prive/IdeaProjects/PianoKeyDetector/resources/IMG_20200922_170508.jpg"
            ),
    Profile("VID_20200922_223905.mp4 1.0",  # 2
            start_location=(360, 450),
            x_increment=13,
            y_increment=-1,
            a=1.005,
            b=1.000,
            c=1.000,
            brightness_threshold=get_average_brightness_for(220, 360),
            default_file_name="/home/prive/IdeaProjects/PianoKeyDetector/resources/VID_20200922_223905.mp4",
            zone_bounds=[[100, 249],
                         [1920, 705], ],
            minimal_contour_area=50,
            calibration_delay_between_keys=0.0,
            calibration_key_start_delay=0.0,
            calibration_key_stop_delay=0.11,
            key_points_filter_standard_deviation=[15, 15],
            contour_brightness_threshold=80,
            ),
    Profile("VID_20200924_100646.mp4 1.0",  # 3
            skip_to_time=5,
            default_file_name="/home/prive/IdeaProjects/PianoKeyDetector/resources/VID_20200924_100646.mp4",
            minimal_contour_area=50,
            calibration_delay_between_keys=0.0,
            calibration_key_start_delay=0.0,
            calibration_key_stop_delay=0.0,
            key_points_filter_standard_deviation=[15, 15],
            contour_brightness_threshold=30,
            ),
    Profile("VID_20200924_100802.mp4 1.0",  # 4
            default_file_name="/home/prive/IdeaProjects/PianoKeyDetector/resources/VID_20200924_100802.mp4",
            skip_to_time=2.5,
            zone_bounds=[[362, 552], [820, 620]],
            mask_area=np.array([[0, 13], [440, 0], [457, 65], [16, 67]]),
            minimal_contour_area=50,
            calibration_delay_between_keys=0.0,
            calibration_key_start_delay=0.0,
            calibration_key_stop_delay=0.0,
            key_points_filter_standard_deviation=[15, 15],
            contour_brightness_threshold=50,
            key_amount_to_calibrate=13,
            ),
    Profile("VID_20200924_100724.mp4 1.0",  # 5
            default_file_name="/home/prive/IdeaProjects/PianoKeyDetector/resources/VID_20200924_100724.mp4",
            skip_to_time=2,
            zone_bounds=[[569, 480], [974, 570]],
            mask_area=np.array([[0, 0], [384, 5], [404, 89], [20, 60]]),
            minimal_contour_area=50,
            calibration_delay_between_keys=0.0,
            calibration_key_start_delay=0.0,
            calibration_key_stop_delay=0.0,
            key_points_filter_standard_deviation=[15, 15],
            contour_brightness_threshold=30,
            key_amount_to_calibrate=23,
            ),
    Profile("Image_screenshot_24.09.2020_keypress.png 1.0",  # 8
            start_location=(360, 450),
            x_increment=13,
            y_increment=-1,
            a=1.005,
            b=1.000,
            c=1.000,
            brightness_threshold=get_average_brightness_for(220, 360),
            default_file_name="/home/prive/IdeaProjects/PianoKeyDetector/Image_screenshot_24.09.2020_keypress.png",
            zone_bounds=[[100, 249],
                         [1920, 705], ],
            minimal_contour_area=50,
            calibration_delay_between_keys=0.0,
            calibration_key_start_delay=0.0,
            calibration_key_stop_delay=0.0,
            key_points_filter_standard_deviation=[60, 60],
            contour_brightness_threshold=40,
            ),
]
