# -*- coding: utf-8 -*-
import argparse
import pathlib

def get_arguments() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Translate a MIDI file to a PWM wave file")
    parser.add_argument("input_file", help="Input MIDI File.")
    args: argparse.Namespace = parser.parse_args()
    args.input_file = pathlib.Path(args.input_file).resolve()
    return args