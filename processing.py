from utils import *

logger = logging.getLogger(__name__)


def paint_keys_detected_chances(frame):
    if not Config.display_debug_info:
        return

    for i, key in enumerate(keys):
        cv2.putText(frame, "{0: <5}".format(key.name),
                    (10, 50 + i * 20), Config.font_family, 0.6, (255, 255, 0), 1, lineType=Config.line_type)
        cv2.putText(frame, "{:0.4f}  ({:0.4f})".format(round(key.detected_chance, 4),
                                                       round(key.highest_detected_chance, 4)),
                    (60, 50 + i * 20), Config.font_family, 0.6, (255, 255, 0), 1, lineType=Config.line_type)


def loop(frame, current_frame_index: int = -1) -> bool:
    # PROCESSING PART
    contours, zone, differences, thresh = get_contours_in_frame(frame)

    if current_frame_index < Config.skip_to_time * 30:
        return True

    detect_keys_from_contours(contours)

    # PAINT PART
    # frame = cv2.addWeighted(zone, 1, thresh, 0.1, 0)

    paint_keys_points(zone)
    paint_contour_outlines(zone, contours)
    paint_pressed_keys(zone)
    paint_keys_detected_chances(frame)

    return show_image(frame)


def detect_keys_from_contours(contours):
    for key in keys:
        if len(contours) == 0:
            key.set_pressed(False)
            continue

        for contour in contours:
            key.check_for_contour(contour)

        key.check_for_contour_finalize()


def paint_pressed_keys(frame: np.ndarray, offset: List = None):
    for key in keys:
        paint_key_on_frame(frame, key, offset)


def paint_key_on_frame(frame: np.ndarray, key: Key, offset: List = None):
    if not key.is_calibrated:
        return

    center_point = key.get_center_point()
    if center_point == (-1, -1):
        return

    draw_point = get_drawing_point_for_point_with_offset(center_point, offset)

    circle_color = Config.key_dot_pressed_color if key.is_pressed else Config.key_dot_not_pressed_color
    cv2.circle(frame, draw_point, Config.key_dot_radius, circle_color,
               Config.key_dot_thickness, lineType=Config.line_type)

    if not key.is_pressed:
        return

    text_margin = Config.text_distance_to_key
    paint_key_name(frame, key, text_margin, offset=offset)
