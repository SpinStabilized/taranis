# -*- coding: utf-8 -*-
"""Taranis, get ready to listen to the ligtning.

Plans - 
    - Collapse tracks to one set of track information and deconflict multiple
    notes so that only one is played per time.
    - Calculate in rests and treat them as notes as well
    - Convert tempo to actual time calculations

"""
from __future__ import annotations
import mido
import pathlib

from typing import Any

import utils.utils as utils

logger = utils.taranis_logger_config()

def note_to_f(note: int, tuning: int=440) -> float: 
    """Convert a MIDI note to frequency.

    Args:
       note: A MIDI note
       tuning: The tuning as defined by the frequency for A4.
    
    Returns:
        The frequency in Hertz of the note.
    """
    return (2**((note-69)/12)) * tuning

class AbsoluteMessage:
    def __init__(self, message: mido.Message, tick: int, tuning: float = 440.0) -> None:
        self.message: mido.Message = message
        self.tick: int = tick
        self.tuning: float = tuning
    
    def __repr__(self) -> str:
        return f'<{repr(self.message)}, tick={self.tick}, f={self.frequency}>'

    @property
    def is_note(self) -> bool:
        return 'note' in self.message.type

    @property
    def frequency(self) -> float:
        """Convert a MIDI note to frequency.

        Args:
        note: A MIDI note
        tuning: The tuning as defined by the frequency for A4.
        
        Returns:
            The frequency in Hertz of the note.
        """
        return (2 ** ((self.message.note - 69) / 12)) * self.tuning if self.is_note else 0.0


def main() -> None:
    logger.info('Taranis starting up.')
    cwd: pathlib.Path = pathlib.Path().absolute()
    test_song1: pathlib.Path = (cwd / 'resources/skye.mid').resolve()
    test_song2: pathlib.Path = (cwd / 'resources/Mortal_Kombat.mid').resolve()

    test_song: pathlib.Path = test_song2

    logger.info(f'Loading {test_song.name}')
    midi = mido.MidiFile(test_song1)

    if len(midi.tracks) == 0:
        logger.error(f'No tracks found in {test_song.name}. Nothing to process.')
    else:
        tempo: int =  mido.bpm2tempo(120)
        tick: int = 0
        notes_track: int = -1
        control_tracks: list[int] = []
        
        for i, track in enumerate(midi.tracks):
            logger.info(f'Processing {test_song.name} track {i}.')
            notes: int = len([msg for msg in track if msg.type == 'note_on' ])
            if notes > 0:
                if notes_track == -1:
                    notes_track = i
                else:
                    logger.warning(f'Track {i} has notes but track {notes_track} already has notes. Track {i} will be ignored.')
            else:
                control_tracks.append(i)
        
        logger.info(f'Notes will be taken from track {notes_track}.')
        logger.info(f'Control messages will also be processed from tracks: {control_tracks}')

        messages_to_ignore: list[str] = [
            'time_signature',
            'key_signature',
            'end_of_track',
            'channel_prefix',
            'program_change',
        ]
        absolute: list[AbsoluteMessage] = []
        for track_number in control_tracks + [notes_track]:
            logger.info(f'Processing track {track_number}.')
            tick = 0
            note_on: int = -1
            for message in midi.tracks[track_number]:
                tick += message.time
                if message.type == 'note_on' and note_on == -1:
                    note_on = message.note
                    absolute.append(AbsoluteMessage(message, tick))
                elif message.type == 'note_on' and note_on != -1:
                    logger.warning(f'Note On when another note is aleady on. Ignoring.')
                elif message.type == 'note_off' and message.note == note_on:
                    note_on = -1
                    absolute.append(AbsoluteMessage(message, tick))
                elif message.type == 'note_off' and message.note != note_on:
                    logger.warning(f'Note Off for note not already on. Ignoring.')
                elif message.type in messages_to_ignore:
                    logger.warning(f'Message of type "{message.type}" ignored.')
                else:
                    absolute.append(AbsoluteMessage(message, tick))
        
        absolute.sort(key=lambda x:x.tick)
        max_ticks: int = absolute[-1].tick
        # print(absolute[:10])


            


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Exiting on Ctrl-C')
        raise SystemExit
    except SystemExit:
        raise