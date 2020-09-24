import logging
import time
from typing import Optional

import cv2
import numpy as np

from config import Config
from models import Key
from project_state import keys
from utils import show_image, get_contour_center, get_contours_in_frame, paint_contour_outlines, \
    paint_keys_points, \
    paint_key_name, paint_contour_centers

logger = logging.getLogger(__name__)

last_calibrated = time.time()
no_more_contours_found_time: Optional[float] = None


def paint_calibration_status_text(frame, text):
    cv2.rectangle(frame, (0, 0), (140, 80), (255, 255, 255), -1)
    cv2.putText(frame, text, (10, 60), Config.font_family, 2, (0, 0, 0), 2, lineType=Config.line_type)


def calibrate_key(frame, key: Key):
    global last_calibrated, no_more_contours_found_time

    # PROCESSING PART
    contours, zone = get_contours_in_frame(frame)[:2]
    contour_centers = get_contours_centers(contours)

    if last_calibrated + Config.calibration_delay_between_keys + Config.calibration_key_start_delay < time.time():
        add_contour_centers_to_key_points(contour_centers, key)

        check_if_calibration_is_done(contours, key)

    # PAINT PART
    if last_calibrated + Config.calibration_delay_between_keys > time.time():
        paint_calibration_status_text(zone, "")
    else:
        paint_calibration_status_text(zone, key.name)

    paint_keys_points(zone)
    paint_contour_outlines(zone, contours)
    paint_contour_centers(zone, contour_centers)
    paint_key_name(zone, key, text_margin=Config.key_brightness_area_size + Config.line_width)

    return show_image(zone)


def check_if_calibration_is_done(contours, key):
    global no_more_contours_found_time, last_calibrated

    if len(contours) > 0 or len(key.points) == 0:
        return

    if no_more_contours_found_time is None:
        no_more_contours_found_time = time.time()
        return

    if no_more_contours_found_time + Config.calibration_key_stop_delay > time.time():
        return

    no_more_contours_found_time = None
    last_calibrated = time.time()

    filter_points_for_key(key)

    if len(key.points) == 0:
        logger.warning("All points are filtered out for key {}. Retrying.".format(key))
        return

    key.is_calibrated = True
    logger.info("Key {} calibrated. Delaying for: {} ms"
                .format(key, Config.calibration_delay_between_keys))


def get_contours_centers(contours):
    return list(get_contour_center(contour) for contour in contours)


def add_contour_centers_to_key_points(contour_centers, key):
    for center in contour_centers:
        if center in key.points:
            continue
        key.points.append(center)


def filter_points_for_key(key):
    logger.info("Applying points filter for key: {}".format(key))

    a = 2
    mean = np.mean(key.points, axis=0)

    if Config.key_points_filter_standard_deviation is not None:
        std = Config.key_points_filter_standard_deviation
    else:
        std = np.std(key.points, axis=0)

    filtered_points = []
    for point in key.points:
        if not (mean[0] + a * std[0] > point[0] > mean[0] - a * std[0]):
            continue
        if not (mean[1] + a * std[1] > point[1] > mean[1] - a * std[1]):
            continue

        filtered_points.append(point)
    key.points = filtered_points


def loop(frame, current_frame_index: int = -1) -> bool:

    if current_frame_index < 5 * 30:
        return True

    try:
        key_to_calibrate = next(key for key in keys if not key.is_calibrated)
    except StopIteration:
        logger.info("Calibration is done")
        return False

    if not calibrate_key(frame, key_to_calibrate):
        return False

    return True  # show_image(frame)


def print_keys():
    print("keys = [")
    for key in keys:
        print("Key(\"{}\", is_calibrated={}, color=({}), key_detected_chance_threshold={}, points=[{}]),"
              .format(key.name, key.is_calibrated,
                      ', '.join(str(round(color)) for color in key.color),
                      round(key.highest_detected_chance * 0.8, 6),
                      ', '.join(str(point) for point in key.points)))
    print("]")
