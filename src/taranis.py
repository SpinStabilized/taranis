# -*- coding: utf-8 -*-
"""Taranis, get ready to listen to the ligtning.


"""
from __future__ import annotations

from mido import MidiFile

test_song1 = '/home/brian/taranis/resources/skye.mid'
test_song2 = '/home/brian/taranis/resources/Mortal_Kombat.mid'
midi = MidiFile(test_song2)

track = midi.tracks[0]

for msg in track:
    print(msg)