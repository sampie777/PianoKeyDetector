import logging
from typing import List

import cv2
import numpy as np

import project_state
from config import Config
from models import Key
from project_state import keys

logger = logging.getLogger(__name__)

background_image_file = cv2.imread(
        "/home/prive/IdeaProjects/PianoKeyDetector/Image_screenshot_24.09.2020_background.png", cv2.IMREAD_COLOR)
background_image = None


def show_image(image, title: str = Config.preview_window_title, delay: int = Config.preview_frame_rate) -> bool:
    cv2.namedWindow(title, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(title, image)

    key = cv2.waitKey(delay)
    if key in [27, 13, 32]:
        return False
    return True


def get_contour_center(contour):
    momentum = cv2.moments(contour)
    x = int(momentum["m10"] / momentum["m00"])
    y = int(momentum["m01"] / momentum["m00"])
    return x, y


def paint_contour_outlines(frame, contours, offset: List = None):
    for i, contour in enumerate(contours):
        if offset is not None:
            contour = np.add(offset, contour)

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 1)
        cv2.drawContours(frame, [contour], 0, (0, 100, 255), 1)
        cv2.putText(frame, str(i), (x + w + 5, y + h), Config.font_family, 0.8, (200, 0, 200), 1)


def prepare_frame(frame):
    global background_image
    if background_image is None and Config.profile.name == "Image_screenshot_24.09.2020_keypress.png 1.0":
        frame = background_image_file.copy()

    zone = frame[Config.zone_bounds[0][1]:Config.zone_bounds[1][1], Config.zone_bounds[0][0]:Config.zone_bounds[1][0]]

    mask_area = project_state.mask_area
    if mask_area is None:
        mask_area = np.array([(120, 400),
                              (1690, 270),
                              (1710, 417),
                              (141, 430)])

    cv2.drawContours(zone, [mask_area], 0, (255, 255, 255), 1)

    mask = np.zeros_like(zone)
    cv2.drawContours(mask, [mask_area], 0, (255, 255, 255), -1)
    masked = np.zeros_like(zone)
    masked[mask == 255] = zone[mask == 255]

    gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)
    blurred = cv2.GaussianBlur(blurred, (9, 9), 0)

    if background_image is None:
        logger.info("Set background image")
        background_image = blurred
        return zone, blurred, True

    return zone, blurred, False


def get_contours_in_frame(frame):
    zone, blurred, is_background = prepare_frame(frame)
    if is_background:
        return [], zone, zone, zone

    # differences = cv2.subtract(blurred, background_image)
    differences = cv2.absdiff(background_image, blurred)

    thresh = cv2.threshold(differences, Config.contour_brightness_threshold, 255, cv2.THRESH_BINARY)[1]
    # thresh = cv2.dilate(thresh, None, iterations=2)
    # thresh = cv2.erode(thresh, None, iterations=2)

    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = list(filter(lambda c: cv2.contourArea(c) > Config.minimal_contour_area, contours))

    differences = cv2.cvtColor(differences, cv2.COLOR_GRAY2BGR)
    thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    return contours, zone, differences, thresh


def paint_keys_points(frame, offset: List = None):
    for key in keys:

        if key.line is not None:
            start_point = key.line[0]
            stop_point = key.line[1]
            if offset is not None:
                start_point = tuple(np.add(offset, start_point))
                stop_point = tuple(np.add(offset, stop_point))

            cv2.line(frame, start_point, stop_point, key.color, Config.key_line_thickness)

            if not Config.paint_key_points_if_line_available:
                continue

        for point in key.points:
            if offset is not None:
                point = tuple(np.add(point, offset))

            cv2.circle(frame, point, Config.key_point_radius, key.color,
                       Config.key_point_thickness, lineType=Config.line_type)


def paint_key_name(frame, key: Key, text_margin: int, offset: List = None):
    center_point = key.get_center_point()
    if center_point == (-1, -1):
        return

    draw_point = get_drawing_point_for_point_with_offset(center_point, offset)

    # Draw shadow
    cv2.putText(frame, key.name, (draw_point[0] + text_margin, draw_point[1] - text_margin),
                Config.font_family, Config.key_name_font_scale,
                (0, 0, 0),
                round(Config.key_name_font_thickness * 1.4), Config.line_type)
    # Draw text
    cv2.putText(frame, key.name, (draw_point[0] + text_margin, draw_point[1] - text_margin),
                Config.font_family, Config.key_name_font_scale,
                key.color,
                Config.key_name_font_thickness, Config.line_type)


def get_drawing_point_for_point_with_offset(draw_point, offset):
    draw_point = (round(draw_point[0]), round(draw_point[1]))
    if offset is not None:
        draw_point = tuple(np.add(draw_point, offset))
    return draw_point


def paint_contour_centers(frame, contour_centers, offset: List = None):
    for center_point in contour_centers:
        if offset is not None:
            center_point = tuple(np.add(center_point, offset))

        cv2.circle(frame, center_point, Config.contour_center_radius, (255, 0, 0),
                   Config.contour_center_thickness, lineType=Config.line_type)


def best_fit_slope_and_intercept(xs: np.ndarray, ys: np.ndarray):
    # https://pythonprogramming.net/how-to-program-best-fit-line-machine-learning-tutorial/
    # y(x) = m * x + b
    m_denominator = np.mean(xs) * np.mean(xs) - np.mean(xs * xs)
    if m_denominator == 0:
        m = 0
    else:
        m = (np.mean(xs) * np.mean(ys) - np.mean(xs * ys)) / m_denominator

    b = np.mean(ys) - m * np.mean(xs)

    return m, b
