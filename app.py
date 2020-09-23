import logging
import sys
from typing import List

import cv2
import numpy as np

from config import Config
from models import Key

logger = logging.getLogger(__name__)

logging.basicConfig(
        format='[%(levelname)s] %(asctime)s %(name)s | %(message)s',
        level=Config.log_level)

keys: List[Key] = []
note_base_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def main(args: List):
    logger.info("Starting application")
    Config.load_profile("IMG_20200922_170508.jpg 1.0")
    # Config.load_profile("IMG_20200922_170508.jpg 2.0")
    # Config.load_profile("VID_20200922_223905.mp4 1.0")

    handle_command_args(args)
    Config.calibration = True

    generate_keys()

    # setup video input
    capture = setup_video_input()

    if Config.record_output:
        logger.info("Creating video writer")
        video_writer = cv2.VideoWriter('/home/prive/IdeaProjects/PianoKeyDetector/output.mp4',
                                       cv2.VideoWriter_fourcc(*'MPEG'), 24.0,
                                       (capture.get(cv2.CAP_PROP_FRAME_WIDTH), capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    while True:
        ret, frame = get_frame(capture)
        if not ret or frame is None:
            logger.info("No new frame found, exiting loop")
            break

        if not loop(frame):
            logger.info("Loop exited")
            break

        if Config.record_output:
            video_writer.write(frame)

    if not Config.is_image:
        logger.info("Releasing capture")
        capture.release()

    if Config.record_output:
        logger.info("Releasing video writer")
        video_writer.release()

    cv2.destroyAllWindows()
    logger.info("Application finished")


def generate_keys():
    global keys
    # keys = [
    #     Key("B3", 1675, 1924),
    #     Key("C3", 1678, 1966),
    #     Key("D3", 1681, 2008),
    #     Key("E3", 1684, 2050),
    # ]

    # start_location = (1390, 1571)

    # start_location = (1675, 1924)
    # start_location = (1550, 1571)

    start_location = Config.profile.start_location
    x_increment = Config.profile.x_increment
    y_increment = Config.profile.y_increment
    a = Config.profile.a
    b = Config.profile.b
    c = Config.profile.c

    keys.clear()
    for i in range(0, 30):
        note_name = note_base_names[i % 12] + str(i // 12)
        keys.append(
                Key(note_name, round(start_location[0] + i * x_increment), round(start_location[1] + i * y_increment)))

        x_increment *= a
        y_increment *= a

        a *= b
        b *= c


def handle_command_args(args: list):
    Config.file_name = args[0] if len(args) > 0 else Config.default_file_name
    Config.gray_scale = "--color" in args
    Config.calibration = "--calibrate" in args
    Config.record_output = "--record" in args

    logger.info("Config.FILE_NAME={}".format(Config.file_name))
    logger.info("Config.GRAY_SCALE={}".format(Config.gray_scale))
    logger.info("Config.CALIBRATION={}".format(Config.calibration))
    logger.info("Config.RECORD_OUTPUT={}".format(Config.record_output))


def setup_video_input():
    Config.is_image = ".jpg" in Config.file_name or ".png" in Config.file_name
    logger.info("Config.IS_IMAGE={}".format(Config.is_image))

    if Config.is_image:
        logger.info("Opening image file: {}".format(Config.file_name))
        capture = cv2.imread(Config.file_name, cv2.IMREAD_GRAYSCALE if Config.gray_scale else cv2.IMREAD_COLOR)
    else:
        logger.info("Opening video file: {}".format(Config.file_name))
        capture = cv2.VideoCapture(Config.file_name)

    if capture is None:
        logger.error("Failed to open file: {}".format(Config.file_name))
        sys.exit("Failed to open file: {}".format(Config.file_name))

    return capture


def get_frame(capture):
    if Config.is_image:
        ret = True
        frame = capture.copy()
    else:
        ret, frame = capture.read()

    return ret, frame


def loop(frame) -> bool:
    detect_key_presses_for_frame(frame)

    key_presses: List[Key] = list(filter(lambda key: key.pressed, keys))

    return display_pressed_keys(key_presses, frame)


def detect_key_presses_for_frame(frame):
    for key in keys:
        key.is_pressed_in_frame(frame)


def display_pressed_keys(key_presses, frame) -> bool:
    key_presses_names: List[str] = list(map(lambda key: key.name, key_presses))

    if not Config.calibration:
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
                Config.text_font, Config.font_scale,
                (0, 0, 0),
                round(Config.font_thickness * 1.4), Config.line_type)
    # Draw text
    cv2.putText(frame, key.name, (key.x + text_margin, key.y - text_margin),
                Config.text_font, Config.font_scale,
                Config.font_color,
                Config.font_thickness, Config.line_type)


def show_image(image, title: str = "Image", delay: int = Config.preview_frame_rate) -> bool:
    cv2.namedWindow(title, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(title, image)

    key = cv2.waitKey(delay)
    if key in [27, 13, 32]:
        return False
    return True


if __name__ == "__main__":
    main(sys.argv[1:])
