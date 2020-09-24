import logging
from typing import List

import cv2
import numpy as np

import output
from config import Config
from models import Key
from project_state import keys
from utils import show_image, get_contours_in_frame, paint_key_name, paint_keys_points, \
    get_drawing_point_for_point_with_offset, paint_contour_outlines

logger = logging.getLogger(__name__)


def paint_keys_detected_chances(frame):
    for i, key in enumerate(keys):
        cv2.putText(frame, "{0: <5}".format(key.name),
                    (10, 50 + i * 20), Config.font_family, 0.6, (255, 255, 0), 1, lineType=cv2.LINE_AA)
        cv2.putText(frame, "{:0.4f}  ({:0.4f})".format(round(len(key.points), 4),
                                                       round(key.highest_detected_chance, 4)),
                    (60, 50 + i * 20), Config.font_family, 0.6, (255, 255, 0), 1, lineType=cv2.LINE_AA)


def loop(frame, current_frame_index: int = -1) -> bool:
    # PROCESSING PART
    # detect_key_presses_for_frame(frame)

    contours, zone, differences, thresh = get_contours_in_frame(frame)

    if current_frame_index < 5 * 30:
        return True

    detect_keys_from_contours(contours)

    key_presses: List[Key] = list(filter(lambda key: key.is_pressed, keys))
    # print(len(key_presses))

    # OUTPUT PART
    output.write_key_presses_to_midi(current_frame_index)

    # PAINT PART
    frame = cv2.addWeighted(zone, 1, thresh, 0.1, 0)

    paint_contour_outlines(frame, contours)
    paint_keys_points(frame)#, offset=Config.zone_bounds[0])
    paint_keys_detected_chances(frame)

    return display_pressed_keys(frame, key_presses)#, offset=Config.zone_bounds[0])


def detect_key_presses_for_frame(frame):
    for key in keys:
        key.is_pressed_in_frame(frame)


def detect_keys_from_contours(contours):
    for key in keys:
        if len(contours) == 0:
            key.set_pressed(False)
            continue

        for contour in contours:
            key.check_for_contour(contour)

        key.check_for_contour_finalize()


def display_pressed_keys(frame, key_presses, offset: List = None) -> bool:
    if not Config.show_preview_video:
        key_presses_names: List[str] = list(map(lambda key: key.name, key_presses))
        print(' '.join(key_presses_names))
        return True

    for key in keys:
        try:
            paint_key_on_frame(frame, key, offset)
        except:
            pass

    return show_image(frame)


def paint_key_on_frame(frame, key, offset: List = None):
    circle_color = Config.pressed_color if key.is_pressed else Config.not_pressed_color

    draw_point = get_drawing_point_for_point_with_offset(np.mean(key.points, axis=0), offset)

    cv2.circle(frame, draw_point, Config.key_brightness_area_size + Config.line_width // 2, circle_color,
               Config.line_width, lineType=Config.line_type)

    if not key.is_pressed:
        return

    text_margin = Config.key_brightness_area_size + Config.line_width + 10
    paint_key_name(frame, key, text_margin, offset=offset)
