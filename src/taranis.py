# -*- coding: utf-8 -*-
"""Taranis, get ready to listen to the ligtning.

"""
from __future__ import annotations
import argparse
import mido
import pathlib
import rich.console
import rich.progress
import struct
import wave

from typing import Any

import utils
import taranislib


console: rich.console.Console = rich.console.Console()

def main() -> None:
    args: argparse.Namespace = utils.get_arguments()
    if args.verbosity > 0:
        console.log('Taranis starting up.')

    if args.verbosity > 0:
        console.log(f'Loading [i]{args.input_file.name}[/]')
    midi = mido.MidiFile(args.input_file)

    if len(midi.tracks) == 0:
        console.log(f'[bold red]ERROR[/]: No tracks found in [i]{args.input_file.name}[/]. Nothing to process.')
        return
    
    notes_track: int = -1
    control_tracks: list[int] = []
    
    for i, track in enumerate(midi.tracks):
        if args.verbosity > 0:
            console.log(f'Processing [i]{args.input_file.name}[/i] track {i}.')
        notes: int = len([msg for msg in track if msg.type == 'note_on' ])
        if notes > 0:
            if notes_track == -1:
                notes_track = i
            else:
                console.log(f'[bold yellow]WARNING[/i]: Track {i}({midi.tracks[i].name}) has notes but track {notes_track}({midi.tracks[notes_track].name}) already has notes. Track {i}({midi.tracks[i].name}) will be ignored.')
        else:
            control_tracks.append(i)

    console.log(f'Notes will be taken from track {notes_track} ({midi.tracks[notes_track].name}).')
    if control_tracks:
        console.log(f'Control messages will also be processed from tracks: {control_tracks}')

    note_messages: list[taranislib.TaranisMessage] = []
    control_messages: list[taranislib.TaranisMessage] = []
    for track_number in control_tracks + [notes_track]:
        console.log(f'Processing track {track_number} ({midi.tracks[track_number].name}).')
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
                    if args.verbosity > 2:
                        console.log(f'Note On {note_on}')
                elif message.type == 'note_on' and message.velocity == 0 and message.note == note_on:
                    note_on = -1
                    message.tick = tick
                    note_messages.append(message)
                    if args.verbosity > 2:
                        console.log(f'Note Off Via Velocity 0 - {message.note}') 
                elif message.type == 'note_on' and note_on != -1:
                    if args.verbosity > 1:
                        console.log(f'[bold yellow]WARNING[/i]: Note On ({message.note}) when another note ({note_on}) is aleady on. Ignoring.')              
                elif message.type == 'note_off' and message.note == note_on:
                    note_on = -1
                    message.tick = tick
                    note_messages.append(message)
                    if args.verbosity > 2:
                        console.log(f'Note Off {message.note}')
                elif message.type == 'note_off' and message.note != note_on:
                    if args.verbosity > 1:
                        console.log(f'[bold yellow]WARNING[/i]: Note Off ({message.note}) for note not already on. Ignoring.')
            else:
                message.tick = tick
                control_messages.append(message)
    
    control_messages.sort(reverse=True, key=lambda message: message.tick)
    note_messages.reverse()

    with console.status(f'Starting score generation.', spinner='clock'):
        tempo: int =  mido.bpm2tempo(120)
        ticks_per_beat: int = midi.ticks_per_beat
        console.log(f'Ticks/Beat = {ticks_per_beat}')
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
                        console.log(f'Setting tempo to {tempo} ({mido.tempo2bpm(tempo):.0f} BPM).')
                    case 'program_change' | 'control_change':
                        # Control Messages that are not processed
                        if args.verbosity > 2:
                            console.log(f'Ignoring "{m.type}" message.')
                    case 'channel_prefix' | 'end_of_track' | 'key_signature' | 'time_signature' | 'track_name' | 'midi_port':
                        # Meta Message Processing
                        if args.verbosity > 2:
                            console.log(f'Ignoring "{m.type}" meta message')
                    case _:
                        console.log(f'Unknown Control Message: "{m.message}"')

            elif note_messages and note_messages[-1].tick == t:
                m = note_messages.pop()
                match m.type:
                    case 'note_on':
                        if m.velocity != 0:
                            if current_note:
                                console.log(f'Ignoring "note_on" at tick {m.tick} as a note is already on.')
                            else:
                                current_note = taranislib.Note(t, m.note, tempo=tempo, ticks_per_beat=ticks_per_beat)
                                if args.verbosity > 2:
                                    console.log(f'Note {m.note} on at tick {t}')
                        else:
                            if current_note and current_note.note_number == m.note:
                                current_note.end = t
                                score_notes.append(current_note)
                                current_note = None
                                if args.verbosity > 2:
                                    console.log(f'Note {m.note} velocity zero at tick {t}')
                            elif current_note and current_note.note_number != m.note:
                                if args.verbosity > 1:
                                    console.log(f'Ignoring "note_off" at tick {m.tick} that does not match currently on note.')
                            else:
                                if args.verbosity > 1:
                                    console.log(f'Ignoring "note_off" at tick {m.tick} when no note is on.')
                                            
                    case 'note_off':
                        if current_note and current_note.note_number == m.note:
                            current_note.end = t
                            score_notes.append(current_note)
                            current_note = None
                            if args.verbosity > 2:
                                console.log(f'Note {m.note} off at tick {t}')
                        elif current_note and current_note.note_number != m.note:
                            if args.verbosity > 1:
                                console.log(f'Ignoring "note_off" at tick {m.tick} that does not match currently on note.')
                        else:
                            if args.verbosity > 1:
                                console.log(f'Ignoring "note_off" at tick {m.tick} when no note is on.')
                    case _:
                        console.log(f'[bold yellow]WARNING[/i]: Ignoring note message "{m.type}" that I don\'t know how to process.')

            else:
                t += 1

    with console.status(f'Starting score generation.', spinner='clock'):
        t = 0
        score: list[taranislib.Note] = []
        for n in score_notes:
            delta = n.start - t
            if delta > 1:
                rest = taranislib.Rest(t, n.start, tempo=tempo, ticks_per_beat=ticks_per_beat)
                score.append(rest)
            t = n.end + 1
            score.append(n)

    rate = 44100
    audio: list[int] = []
    for n in score:
        audio += n.get_samples(rate)

    output_file: pathlib.Path = args.input_file.parent / (args.input_file.stem + '.wav')
    wav_file = wave.open(str(output_file),"w")

    nchannels = 1               # mono
    samp_width = 2              # 16-bit samples (2 bytes)
    nframes = len(audio)
    comptype = "NONE"           # The only value supported by the python wave module
    compname = "not" # The only value supported by the python wave module
    wav_file.setparams((nchannels, samp_width, rate, nframes, comptype, compname))

    console.log(f'Writing to [i]{args.input_file.stem + ".wav"}[/].')
    for sample in rich.progress.track(audio, description="Writing WAV File"):
        wav_file.writeframes(struct.pack('h', sample))

    wav_file.close()
    console.log(f'Conversion Complete')
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.log('Exiting on Ctrl-C')
        raise SystemExit
    except SystemExit:
        raise