# -*- coding: utf-8 -*-
"""Taranis, get ready to listen to the ligtning.

Plans - 
    - Collapse tracks to one set of track information and deconflict multiple
    notes so that only one is played per time.
    - Calculate in rests and treat them as notes as well
    - Convert tempo to actual time calculations

"""
from __future__ import annotations

from mido import MidiFile

test_song1 = '/home/brian/taranis/resources/skye.mid'

midi = MidiFile(test_song1)

tracks = midi.tracks[1]

for msg in track:
    print(msg, msg.type)

def note_to_f(note: int, tuning: int=440) -> float: 
    """Convert a MIDI note to frequency.

    Args:
       note: A MIDI note
       tuning: The tuning as defined by the frequency for A4.
    
    Returns:
        The frequency in Hertz of the note.
    """
    return (2**((note-69)/12)) * tuning


# Aaronaught
# https://stackoverflow.com/questions/2038313/converting-midi-ticks-to-actual-playback-seconds
# The formula is 60000 / (BPM * PPQ) (milliseconds).

# Where BPM is the tempo of the track (Beats Per Minute).

# (i.e. a 120 BPM track would have a MIDI time of (60000 / (120 * 192)) or
# 2.604 ms for 1 tick.

# If you don't know the BPM then you'll have to determine that first. MIDI
# times are entirely dependent on the track tempo.