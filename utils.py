import cv2

from config import Config
from project_state import keys

background_image = None


def show_image(image, title: str = "Image", delay: int = Config.preview_frame_rate) -> bool:
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


def paint_contour_outlines(contours, frame):
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 1)
        cv2.drawContours(frame, [contour], 0, (0, 255, 0), 3)


def get_objects_in_frame(frame):
    global background_image

    zone = frame[Config.zone_bounds[0][1]:Config.zone_bounds[1][1], Config.zone_bounds[0][0]:Config.zone_bounds[1][0]]
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


def paint_pressed_keys_points(frame):
    for i, key in enumerate(keys):
        prev_point = None
        for point in key.points:
            if prev_point is None:
                prev_point = point
                continue

            a = (i + 1) / len(keys)
            cv2.line(frame, prev_point, point, (255, 255 * a, 255 - 255 * a), 1, lineType=cv2.LINE_AA)
            prev_point = point


def paint_key_name(frame, key, text_margin):
    if len(key.points) == 0:
        return

    # Draw shadow
    cv2.putText(frame, key.name, (key.points[0][0] + text_margin, key.points[0][1] - text_margin),
                Config.font_family, Config.font_scale,
                (0, 0, 0),
                round(Config.font_thickness * 1.4), Config.line_type)
    # Draw text
    cv2.putText(frame, key.name, (key.points[0][0] + text_margin, key.points[0][1] - text_margin),
                Config.font_family, Config.font_scale,
                Config.font_color,
                Config.font_thickness, Config.line_type)


def paint_contour_centers(frame, contour_centers):
    for c in contour_centers:
        cv2.circle(frame, c, 5, (255, 0, 0), -1, lineType=cv2.LINE_AA)
