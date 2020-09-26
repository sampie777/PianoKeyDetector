import logging
import sys
from typing import List

import cv2

import calibration
import output
import processing
import profiles
import project_state
from config import Config
from models import Key
from project_state import keys

logger = logging.getLogger(__name__)

logging.basicConfig(
        format='[%(levelname)s] %(asctime)s %(name)s | %(message)s',
        level=Config.log_level)


def main(args: List):
    logger.info("Starting application")

    Config.load_profile(profiles.profiles[3].name)
    Config.update_project_state()

    handle_command_args(args)
    Config.calibrating = True
    # Config.save_to_video = True

    load_keys()

    # setup video input
    capture = setup_video_input()

    # setup outputs
    output.setup_outputs()

    # setup processing stuff
    if Config.calibrating:
        calibration.setup()

    current_frame_index = -1
    while True:
        try:
            current_frame_index += 1
            ret, frame = get_frame(capture)
            if not ret or frame is None:
                logger.info("No new frame found, exiting loop")
                break

            if Config.calibrating:
                if not calibration.loop(frame, current_frame_index):
                    logger.info("Loop exited")
                    break
            else:
                if not processing.loop(frame, current_frame_index):
                    logger.info("Loop exited")
                    break

            output.write_output_frame(current_frame_index, frame)

        except KeyboardInterrupt:
            logger.info("Exiting loop: KeyboardInterrupt")
            break

    output.save_outputs()

    if not project_state.is_image:
        logger.info("Releasing capture")
        capture.release()

    cv2.destroyAllWindows()
    logger.info("Application finished")


def load_keys():
    if Config.calibrating:
        keys.clear()

    if len(keys) > 0:
        return

    # Generate keys
    key_amount = Config.key_amount_to_calibrate
    for i in range(0, key_amount):
        color_diff = (i + 1) / key_amount * 6.3
        color_diff %= 1
        key_color = (255, 255 * color_diff, 255 - 255 * color_diff)

        note_name = Key.note_base_names[i % 12] + str(i // 12)

        keys.append(Key(note_name, color=key_color))


def handle_command_args(args: list):
    Config.file_name = args[0] if len(args) > 0 else Config.default_file_name
    Config.calibrating = "--calibrate" in args
    Config.save_to_video = "--record" in args

    logger.info("Config.file_name={}".format(Config.file_name))
    logger.info("Config.show_preview_video={}".format(Config.show_preview_video))
    logger.info("Config.calibration={}".format(Config.calibrating))
    logger.info("Config.record_output={}".format(Config.save_to_video))


def setup_video_input():
    project_state.is_image = ".jpg" in Config.file_name or ".png" in Config.file_name
    logger.info("project_state.is_image={}".format(project_state.is_image))

    if project_state.is_image:
        logger.info("Opening image file: {}".format(Config.file_name))
        capture = cv2.imread(Config.file_name, cv2.IMREAD_COLOR)
    else:
        logger.info("Opening video file: {}".format(Config.file_name))
        capture = cv2.VideoCapture(Config.file_name)

        project_state.fps = capture.get(cv2.CAP_PROP_FPS)
        logger.info("Video capture FPS: {}".format(project_state.fps))
        logger.info("Video capture frame count: {}".format(capture.get(cv2.CAP_PROP_FRAME_COUNT)))

    if capture is None:
        logger.error("Failed to open file: {}".format(Config.file_name))
        sys.exit("Failed to open file: {}".format(Config.file_name))

    project_state.frame_shape = (round(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                 round(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    return capture


def get_frame(capture):
    if project_state.is_image:
        ret = True
        frame = capture.copy()
    else:
        ret, frame = capture.read()

    return ret, frame


if __name__ == "__main__":
    main(sys.argv[1:])
