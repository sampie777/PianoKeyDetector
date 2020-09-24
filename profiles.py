from typing import List, Optional


class Profile:
    def __init__(self, name: str,
                 start_location: tuple,
                 x_increment: float = 0,
                 y_increment: float = 0,
                 a: float = 1,
                 b: float = 1,
                 c: float = 1,
                 brightness_threshold: int = 0,
                 default_file_name: Optional[str] = None,
                 zone_bounds: List = None,
                 minimal_contour_area: int = 0,
                 calibration_delay_between_keys: float = 0,
                 calibration_key_start_delay: float = 0,
                 calibration_key_stop_delay: float = 0,
                 key_points_filter_standard_deviation: List = None,
                 contour_brightness_threshold: int = 0,
                 ):
        self.name = name
        self.start_location = start_location
        self.x_increment = x_increment
        self.y_increment = y_increment
        self.a = a
        self.b = b
        self.c = c
        self.brightness_threshold = brightness_threshold
        self.default_file_name = default_file_name

        self.zone_bounds: List = zone_bounds if zone_bounds is not None else [[0, 0], [0, 0]]
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
    Profile("IMG_20200922_170508.jpg 1.0",
            start_location=(1390, 1571),
            x_increment=7,
            y_increment=35,
            a=1.002,
            b=1.0005,
            c=1.00005,
            brightness_threshold=get_average_brightness_for(412, 489),
            default_file_name="/home/prive/IdeaProjects/PianoKeyDetector/resources/IMG_20200922_170508.jpg"
            ),
    Profile("IMG_20200922_170508.jpg 2.0",
            start_location=(1550, 1571),
            x_increment=13,
            y_increment=42,
            a=1.002,
            b=1.0005,
            c=1.00005,
            brightness_threshold=get_average_brightness_for(412, 489),
            default_file_name="/home/prive/IdeaProjects/PianoKeyDetector/resources/IMG_20200922_170508.jpg"
            ),
    Profile("VID_20200922_223905.mp4 1.0",
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
    Profile("VID_20200924_100646.mp4 1.0",
            start_location=(360, 450),
            x_increment=13,
            y_increment=-1,
            a=1.005,
            b=1.000,
            c=1.000,
            brightness_threshold=get_average_brightness_for(220, 360),
            default_file_name="/home/prive/IdeaProjects/PianoKeyDetector/resources/VID_20200924_100646.mp4",
            zone_bounds=[[100, 249],
                         [1920, 705], ],
            minimal_contour_area=50,
            calibration_delay_between_keys=0.0,
            calibration_key_start_delay=0.0,
            calibration_key_stop_delay=0.1,
            key_points_filter_standard_deviation=[15, 15],
            contour_brightness_threshold=40,
            ),
    Profile("VID_20200924_100802.mp4 1.0",
            start_location=(360, 450),
            x_increment=13,
            y_increment=-1,
            a=1.005,
            b=1.000,
            c=1.000,
            brightness_threshold=get_average_brightness_for(220, 360),
            default_file_name="/home/prive/IdeaProjects/PianoKeyDetector/resources/VID_20200924_100802.mp4",
            zone_bounds=[[100, 249],
                         [1920, 705], ],
            minimal_contour_area=50,
            calibration_delay_between_keys=0.0,
            calibration_key_start_delay=0.0,
            calibration_key_stop_delay=0.0,
            key_points_filter_standard_deviation=[60, 60],
            contour_brightness_threshold=40,
            ),
    Profile("Image_screenshot_24.09.2020_keypress.png 1.0",
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
