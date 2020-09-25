import logging
from typing import Optional

from midiutil.MidiFile import MIDIFile
import cv2
import numpy as np

# create your MIDI object
import calibration
import project_state
from config import Config
from models import Key
from project_state import keys

logger = logging.getLogger(__name__)

key_states = dict()
first_note_time = None
bpm_conversion = Config.midi_tempo / 60

midi_writer: Optional[MIDIFile] = None
video_writer: Optional[cv2.VideoWriter] = None


def add_note(key: Key, time, duration):
    midi_time = time * bpm_conversion
    duration = duration * bpm_conversion
    info = "{} ({}) at time={:.3f} ({:.3f} s) for {:.3f}".format(key.name, key.midi_pitch, midi_time,
                                                                 time, duration)

    if round(duration, 3) == 0:
        logger.warning("Can't add MIDI note with duration close to zero: {}".format(info))
        return

    if duration < Config.midi_min_note_duration:
        logger.info("Ignoring notes with duration smaller than {}/{}: {}"
                    .format(*Config.midi_min_note_duration.as_integer_ratio(), info))
        return

    logger.info("Adding MIDI note: {}".format(info))
    midi_writer.addNote(Config.midi_track_index, Config.midi_channel, key.midi_pitch, midi_time, duration,
                        Config.midi_volume)


def write_key_presses_to_midi(time: int):
    global first_note_time

    if project_state.is_image:
        return

    time /= project_state.fps

    for key in keys:
        if not key.state_changed():
            continue

        # If pressed, only record timestamp for later duration calculation
        if key.is_pressed:
            if first_note_time is None:
                first_note_time = time
                logger.info("First note time is: {}".format(first_note_time))

            key_states[key.name] = time
            continue

        if key.name not in key_states.keys():
            logger.warning("Key {} is missing in key_states (timestamp) list".format(key.name))
            continue

        try:
            duration = time - key_states[key.name]
            note_start_time = time - duration - first_note_time
            add_note(key, note_start_time, duration)
        except Exception as e:
            logger.exception(e, stack_info=True)
            pass


def midi_save_file(file_name: str = "output.mid"):
    if project_state.is_image:
        return

    logger.info("Saving MIDI file to: {}".format(file_name))
    with open(file_name, 'wb') as file:
        midi_writer.writeFile(file)


def setup_outputs():
    global midi_writer, video_writer

    if Config.save_to_midi:
        midi_writer = MIDIFile(1)  # only 1 track
        midi_writer.addTrackName(Config.midi_track_index, 0, Config.midi_track_name)
        midi_writer.addTempo(Config.midi_track_index, 0, Config.midi_tempo)

    if Config.save_to_video:
        logger.info("Creating video writer")
        video_writer = cv2.VideoWriter(Config.output_video_file_name,
                                       cv2.VideoWriter_fourcc(*Config.output_video_codec),
                                       project_state.fps,
                                       project_state.frame_shape)


def write_output_frame(current_frame_index: int, frame: np.ndarray):
    if Config.save_to_midi:
        write_key_presses_to_midi(current_frame_index)

    if Config.save_to_video:
        video_writer.write(frame)


def save_outputs():
    if Config.calibrating:
        calibration.print_keys()

    if Config.save_to_midi:
        midi_save_file()

    if Config.save_to_video:
        logger.info("Releasing video writer")
        video_writer.release()
