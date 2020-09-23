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
                 default_file_name: Optional[str] = None):
        self.name = name
        self.start_location = start_location
        self.x_increment = x_increment
        self.y_increment = y_increment
        self.a = a
        self.b = b
        self.c = c
        self.brightness_threshold = brightness_threshold
        self.default_file_name = default_file_name


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
            default_file_name="/home/prive/IdeaProjects/PianoKeyDetector/resources/VID_20200922_223905.mp4"
            ),
]
