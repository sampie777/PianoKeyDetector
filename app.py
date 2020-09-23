import logging
import sys
from typing import List

import cv2
import numpy as np

import calibration
import processing
import profiles
from config import Config
from models import Key
from project_state import keys

logger = logging.getLogger(__name__)

logging.basicConfig(
        format='[%(levelname)s] %(asctime)s %(name)s | %(message)s',
        level=Config.log_level)

note_base_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def main(args: List):
    logger.info("Starting application")
    # Config.load_profile("IMG_20200922_170508.jpg 1.0")
    # Config.load_profile("IMG_20200922_170508.jpg 2.0")
    # Config.load_profile("VID_20200922_223905.mp4 1.0")
    Config.load_profile(profiles.profiles[2].name)

    handle_command_args(args)
    # Config.calibration = True
    Config.show_preview_video = True

    generate_keys()

    # setup video input
    capture = setup_video_input()

    if Config.record_output:
        logger.info("Creating video writer")
        video_writer = cv2.VideoWriter('/home/prive/IdeaProjects/PianoKeyDetector/output.mp4',
                                       cv2.VideoWriter_fourcc(*'MPEG'), 24.0,
                                       (capture.get(cv2.CAP_PROP_FRAME_WIDTH), capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    while True:
        try:
            ret, frame = get_frame(capture)
            if not ret or frame is None:
                logger.info("No new frame found, exiting loop")
                break

            if Config.calibration:
                if not calibration.loop(frame):
                    logger.info("Loop exited")
                    break
            else:
                if not processing.loop(frame):
                    logger.info("Loop exited")
                    break

            if Config.record_output:
                video_writer.write(frame)
        except KeyboardInterrupt:
            logger.info("Exiting loop: KeyboardInterrupt")
            break

    if Config.calibration:
        calibration.print_keys()

    if not Config.is_image:
        logger.info("Releasing capture")
        capture.release()

    if Config.record_output:
        logger.info("Releasing video writer")
        video_writer.release()

    cv2.destroyAllWindows()
    logger.info("Application finished")


def generate_keys():
    if len(keys) > 0:
        return

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
    Config.show_preview_video = "--preview" in args
    Config.record_output = "--record" in args

    logger.info("Config.file_name={}".format(Config.file_name))
    logger.info("Config.gray_scale={}".format(Config.gray_scale))
    logger.info("Config.show_preview_video={}".format(Config.show_preview_video))
    logger.info("Config.calibration={}".format(Config.calibration))
    logger.info("Config.record_output={}".format(Config.record_output))


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


if __name__ == "__main__":
    main(sys.argv[1:])
