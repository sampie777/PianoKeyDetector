import logging
import sys
from typing import List

import cv2
import numpy as np

from config import Config
from models import Key
from project_state import keys
from utils import show_image

logger = logging.getLogger(__name__)


def loop(frame) -> bool:
    detect_key_presses_for_frame(frame)

    key_presses: List[Key] = list(filter(lambda key: key.pressed, keys))

    return display_pressed_keys(key_presses, frame)


def detect_key_presses_for_frame(frame):
    for key in keys:
        key.is_pressed_in_frame(frame)


def display_pressed_keys(key_presses, frame) -> bool:
    key_presses_names: List[str] = list(map(lambda key: key.name, key_presses))

    if not Config.show_preview_video:
        print(' '.join(key_presses_names))
        return True

    for key in keys:
        try:
            paint_key_on_frame(frame, key)
        except:
            pass

    return show_image(frame)


def paint_key_on_frame(frame, key):
    circle_color = Config.pressed_color if key.pressed else Config.not_pressed_color

    cv2.circle(frame, (key.x, key.y), Config.key_brightness_area_size + Config.line_width // 2, circle_color,
               Config.line_width, lineType=Config.line_type)

    if not key.pressed:
        return

    text_margin = (Config.key_brightness_area_size + Config.line_width)
    # Draw shadow
    cv2.putText(frame, key.name, (key.x + text_margin, key.y - text_margin),
                Config.font_family, Config.font_scale,
                (0, 0, 0),
                round(Config.font_thickness * 1.4), Config.line_type)
    # Draw text
    cv2.putText(frame, key.name, (key.x + text_margin, key.y - text_margin),
                Config.font_family, Config.font_scale,
                Config.font_color,
                Config.font_thickness, Config.line_type)
