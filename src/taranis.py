# -*- coding: utf-8 -*-
"""Taranis, get ready to listen to the ligtning.

Plans - 
    - Collapse tracks to one set of track information and deconflict multiple
    notes so that only one is played per time.
    - Calculate in rests and treat them as notes as well
    - Convert tempo to actual time calculations

"""
from __future__ import annotations
import argparse
import mido
import pathlib
import struct
import tqdm
import wave

from typing import Any

import utils
import taranislib

logger = utils.taranis_logger_config()

def main() -> None:
    args: argparse.Namespace = utils.get_arguments()
    print(args.input_file)
    logger.info('Taranis starting up.')

    test_song: pathlib.Path = args.input_file

    logger.info(f'Loading {test_song.name}')
    midi = mido.MidiFile(test_song)

    if len(midi.tracks) == 0:
        logger.error(f'No tracks found in {test_song.name}. Nothing to process.')
        return
    
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

    note_messages: list[taranislib.TaranisMessage] = []
    control_messages: list[taranislib.TaranisMessage] = []
    for track_number in control_tracks + [notes_track]:
        logger.info(f'Processing track {track_number}.')
        tick = 0
        note_on: int = -1
        track: mido.MidiTrack = midi.tracks[track_number]
        for mido_message in track:
            message: taranislib.TaranisMessage = taranislib.TaranisMessage(mido_message)
            tick += message.time
            if message.is_note:
                if message.type == 'note_on' and note_on == -1:
                    note_on = message.note
                    message.tick = tick
                    note_messages.append(message)
                    logger.info(f'Note On {note_on}')
                elif message.type == 'note_on' and message.velocity == 0 and message.note == note_on:
                    note_on = -1
                    message.tick = tick
                    note_messages.append(message)
                    logger.warning(f'Note Off Via Velocity 0 - {message.note}') 
                elif message.type == 'note_on' and note_on != -1:
                    logger.warning(f'Note On ({message.note}) when another note ({note_on}) is aleady on. Ignoring.')
                    # pass                 
                elif message.type == 'note_off' and message.note == note_on:
                    note_on = -1
                    message.tick = tick
                    note_messages.append(message)
                    logger.warning(f'Note Off {message.note}')
                elif message.type == 'note_off' and message.note != note_on:
                    # pass
                    logger.warning(f'Note Off ({message.note}) for note not already on. Ignoring.')
            else:
                message.tick = tick
                control_messages.append(message)
    
    control_messages.sort(reverse=True, key=lambda message: message.tick)
    note_messages.reverse()

    logger.info(f'Starting score generation.')
    tempo: int =  mido.bpm2tempo(120)
    ticks_per_beat: int = midi.ticks_per_beat
    logger.info(f'Ticks/Beat = {ticks_per_beat}')
    max_ticks: int = max([m.tick for m in control_messages if m.type == 'end_of_track'])
    score_notes: list[taranislib.Note] = []
    t: int = 0
    current_note: taranislib.Note | None = None
    m: taranislib.TaranisMessage
    while t <= max_ticks:
        if control_messages and control_messages[-1].tick == t:
            m = control_messages.pop()
            match m.type:
                case 'set_tempo':
                    tempo = m.message.dict()['tempo']
                    logger.info(f'Setting tempo to {tempo} ({mido.tempo2bpm(tempo)} BPM).')
                case 'program_change' | 'control_change':
                    # Control Messages that are not processed
                    logger.warning(f'Ignoring "{m.type}" message.')
                case 'channel_prefix' | 'end_of_track' | 'key_signature' | 'time_signature' | 'track_name':
                    # Meta Message Processing
                    logger.warning(f'Ignoring "{m.type}" meta message')
                case _:
                    logger.warning(f'Unknown Control Message: "{m.message}"')

        elif note_messages and note_messages[-1].tick == t:
            m = note_messages.pop()
            match m.type:
                case 'note_on':
                    if m.velocity != 0:
                        if current_note:
                            logger.warning(f'Ignoring "note_on" at tick {m.tick} as a note is already on.')
                        else:
                            current_note = taranislib.Note(t, m.note, tempo=tempo, ticks_per_beat=ticks_per_beat)
                            logger.info(f'Note {m.note} on at tick {t}')
                    else:
                        if current_note and current_note.note_number == m.note:
                            current_note.end = t
                            score_notes.append(current_note)
                            current_note = None
                            logger.info(f'Note {m.note} velocity zero at tick {t}')
                        elif current_note and current_note.note_number != m.note:
                          logger.warning(f'Ignoring "note_off" at tick {m.tick} that does not match currently on note.')
                        else:
                            logger.warning(f'Ignoring "note_off" at tick {m.tick} when no note is on.')
                                           
                case 'note_off':
                    if current_note and current_note.note_number == m.note:
                        current_note.end = t
                        score_notes.append(current_note)
                        current_note = None
                        # logger.info(f'Note {m.note} off at tick {t}')
                    elif current_note and current_note.note_number != m.note:
                        logger.warning(f'Ignoring "note_off" at tick {m.tick} that does not match currently on note.')
                    else:
                        logger.warning(f'Ignoring "note_off" at tick {m.tick} when no note is on.')
                case _:
                    logger.warning(f'Ignoring note message "{m.type}" that I don\'t know how to process.')

        else:
            t += 1

    logger.info('Adding in rests.')
    t = 0
    score: list[taranislib.Note] = []
    for n in score_notes:
        delta = n.start - t
        if delta > 1:
            # logger.info(f'Silence Delta = {delta}')
            rest = taranislib.Rest(t, n.start, tempo=tempo, ticks_per_beat=ticks_per_beat)
            # logger.info(f'Adding a {rest.duration} tick rest at {t} ticks.')
            score.append(rest)
        t = n.end + 1
        
        score.append(n)

    logger.info('Generating audio samples.')
    rate = 44100
    audio: list[int] = []
    for n in score:
        audio += n.get_samples(rate)

    output_file: pathlib.Path = test_song.parent / (test_song.stem + '.wav')
    wav_file = wave.open(str(output_file),"w")

    nchannels = 1               # mono
    samp_width = 2              # 16-bit samples (2 bytes)
    nframes = len(audio)
    comptype = "NONE"           # The only value supported by the python wave module
    compname = "not compressed" # The only value supported by the python wave module
    wav_file.setparams((nchannels, samp_width, rate, nframes, comptype, compname))

    logger.info(f'Writing to {test_song.stem + ".wav"}.')
    for sample in tqdm.tqdm(audio):
        wav_file.writeframes(struct.pack('h', sample))

    wav_file.close()
    logger.info(f'Conversion Complete')
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Exiting on Ctrl-C')
        raise SystemExit
    except SystemExit:
        raise