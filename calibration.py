import logging

import cv2
import numpy as np

from config import Config
from models import Key
from project_state import keys
from utils import show_image

logger = logging.getLogger(__name__)

zone_bounds = [
    [100, 249],
    [1920, 705],
]

background_image = None


def display_calibration_key_text(frame, key: Key):
    cv2.rectangle(frame, (0, 0), (100, 80), (255, 255, 255), -1)
    cv2.putText(frame, key.name, (20, 60), Config.font_family, 2, (0, 0, 0), 2, lineType=Config.line_type)


def get_contour_center(contour):
    momentum = cv2.moments(contour)
    x = int(momentum["m10"] / momentum["m00"])
    y = int(momentum["m01"] / momentum["m00"])
    return x, y


def calibrate_key(frame, key: Key):
    contours, zone = get_objects_in_frame(frame)

    if len(contours) == 0 and len(key.points) > 0:
        key.calibrated = True
        return True

    # draw_contours(contours, zone)

    contour_centers = list(get_contour_center(contour) for contour in contours)
    # for c in contour_centers:
    #     cv2.circle(zone, c, 5, (255, 0, 0), -1, lineType=cv2.LINE_AA)

    # if len(contour_centers) > 0:
    #     key.points.append(contour_centers[0])

    paint_keys(zone)
    display_calibration_key_text(zone, key)
    return show_image(zone)


def draw_contours(contours, frame):
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 1)
        cv2.drawContours(frame, [contour], 0, (0, 255, 0), 3)


def get_objects_in_frame(frame):
    global background_image

    zone = frame[zone_bounds[0][1]:zone_bounds[1][1], zone_bounds[0][0]:zone_bounds[1][0]]
    gray = cv2.cvtColor(zone, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)
    blurred = cv2.GaussianBlur(blurred, (9, 9), 0)

    if background_image is None:
        background_image = blurred
        return [], zone

    differences = cv2.subtract(blurred, background_image)
    thresh = cv2.threshold(differences, 80, 255, cv2.THRESH_BINARY)[1]
    # thresh = cv2.dilate(thresh, None, iterations=2)

    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = list(filter(lambda c: cv2.contourArea(c) > 200, contours))
    return contours, zone


def loop(frame) -> bool:
    key_to_calibrate = next(key for key in keys if not key.calibrated)

    if key_to_calibrate is None:
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


def paint_keys(frame):
    for i, key in enumerate(keys):
        prev_point = None
        for point in key.points:
            if prev_point is None:
                prev_point = point
                continue

            cv2.line(frame, prev_point, point, (255, 255 * (i + 1) // len(keys), 0), 1, lineType=cv2.LINE_AA)
            prev_point = point
