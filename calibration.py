import logging
import time
from typing import Optional

import cv2
import numpy as np

from config import Config
from models import Key
from project_state import keys
from utils import show_image, get_contour_center, get_objects_in_frame, paint_contour_outlines, \
    paint_pressed_keys_points, \
    paint_key_name, paint_contour_centers

logger = logging.getLogger(__name__)

last_calibrated = time.time()


def paint_calibration_key_text(frame, key: Optional[Key]):
    text = "" if key is None else key.name

    cv2.rectangle(frame, (0, 0), (100, 80), (255, 255, 255), -1)
    cv2.putText(frame, text, (20, 60), Config.font_family, 2, (0, 0, 0), 2, lineType=Config.line_type)


def calibrate_key(frame, key: Key):
    global last_calibrated

    contours, zone = get_objects_in_frame(frame)
    contour_centers = get_contours_centers(contours)

    if last_calibrated + Config.calibration_delay_between_keys < time.time():
        paint_calibration_key_text(zone, key)

        if last_calibrated + Config.calibration_delay_between_keys + Config.calibration_key_start_delay < time.time():

            if len(contours) == 0 and len(key.points) > 0:
                key.calibrated = True
                last_calibrated = time.time()
                logger.info("Key {} calibrated. Delaying for: {} ms".format(key, Config.calibration_delay_between_keys))

            add_contour_centers_to_key_points(contour_centers, key)

    else:
        paint_calibration_key_text(zone, None)

    paint_pressed_keys_points(zone)
    paint_contour_outlines(contours, zone)
    paint_contour_centers(zone, contour_centers)
    paint_key_name(zone, key, text_margin=Config.key_brightness_area_size + Config.line_width)

    return show_image(zone)


def get_contours_centers(contours):
    return list(get_contour_center(contour) for contour in contours)


def add_contour_centers_to_key_points(contour_centers, key):
    for center in contour_centers:
        key.points.append(center)


def loop(frame) -> bool:
    try:
        key_to_calibrate = next(key for key in keys if not key.calibrated)
    except StopIteration:
        logger.info("Calibration is done")
        return False

    if not calibrate_key(frame, key_to_calibrate):
        return False

    return True  # show_image(frame)


def print_keys():
    print("keys = [")
    for key in keys:
        print("Key(\"{}\", points=[{}]),".format(key.name, ', '.join(str(point) for point in key.points)))
    print("]")
