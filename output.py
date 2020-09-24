import logging

from midiutil.MidiFile import MIDIFile

# create your MIDI object
import project_state
from config import Config
from models import Key
from project_state import keys

logger = logging.getLogger(__name__)

ticks_per_quarternote = 960
midi_file = MIDIFile(1, ticks_per_quarternote)  # only 1 track
track = 0  # the only track

time = 0  # start at the beginning
midi_file.addTrackName(track, time, "Sample Track")
tempo = 120
midi_file.addTempo(track, time, tempo)

# add some notes
channel = 0
volume = 100

bpm_conversion = (tempo / 60)


key_states = dict()
first_note_time = None


def add_note(key: Key, time, duration):
    midi_time = time * bpm_conversion
    duration = duration * bpm_conversion
    logger.info(
        "Adding MIDI note: {} ({}) at time={:.3f} ({:.3f} s) for {:.3f}".format(key.name, key.midi_pitch, midi_time,
                                                                                time, duration))
    midi_file.addNote(track, channel, key.midi_pitch, midi_time, duration, volume)


def write_key_presses_to_midi(time: int):
    global first_note_time

    if Config.is_image:
        return

    time /= project_state.fps

    for key in keys:
        if not key.state_changed():
            continue

        if key.is_pressed:
            if first_note_time is None:
                first_note_time = time
                logger.info("First note time is: {}".format(first_note_time))

            key_states[key.name] = time
            continue

        if key.name not in key_states.keys():
            logger.warning("Key {} is missing in key_states list".format(key.name))
            continue

        try:
            duration = time - key_states[key.name]
            add_note(key, time - duration - first_note_time, duration)
        except Exception as e:
            logger.exception(e, stack_info=True)
            pass


def midi_save_file(file_name: str = "output.mid"):
    if Config.is_image:
        return

    logger.info("Saving MIDI file to: {}".format(file_name))
    with open(file_name, 'wb') as file:
        midi_file.writeFile(file)
