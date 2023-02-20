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

def main():
    logger.info('Taranis starting up.')
    test_song1: pathlib.Path = pathlib.Path('../resources/skye.mid')
    test_song2: pathlib.Path = pathlib.Path('../resources/Mortal_Kombat.mid')

    test_song: pathlib.Path = test_song2

    logger.info(f'Loading {test_song}')
    midi = mido.MidiFile(test_song1)

    if len(midi.tracks) == 0:
        logger.error(f'No tracks found in {test_song}. Nothing to process.')
    else:
        tempo: int =  mido.bpm2tempo(120)
        tick: int = 0
        for i, track in enumerate(midi.tracks):
            logger.info(f'Processing {test_song} track {i}.')

            for msg in track[:5]:
                print(msg)



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Exiting on Ctrl-C')
        raise SystemExit
    except SystemExit:
        raise