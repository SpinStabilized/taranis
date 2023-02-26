# -*- coding: utf-8 -*-
import math
import mido

class Note:
    def __init__(self, start: int, note_number: int, tempo: int = 500000, ticks_per_beat: int = 0, tuning: int = 440):
        self._start: int = start
        self._end: int = start
        self._note_number: int = note_number
        self.tempo: int = tempo
        self.ticks_per_beat: int = ticks_per_beat
        self.tuning: int = tuning
    
    def __repr__(self) -> str:
        return f'<taranislib.Note {self.note_number}@{self.start}:{self.end}>'

    @property
    def start(self) -> int:
        return self._start
    @start.setter
    def start(self, start: int) -> None:
        if start < 0:
            pass # raise an exception
        else:
            self._start = start
    
    @property
    def end(self) -> int:
        return self._end
    @end.setter
    def end(self, end: int) -> None:
        if end < self.start:
            pass # raise an exception
        else:
            self._end = end
    
    @property
    def note_number(self) -> int:
        return self._note_number
    @note_number.setter
    def note_number(self, note_number: int) -> None:
        if note_number < 12 or note_number > 127:
            pass # raise an exception
        else:
            self._note_number = note_number
    
    @property
    def duration(self) -> int:
        return self.end - self.start
    
    @property
    def duration_s(self) -> float:
        return mido.tick2second(self.duration, self.ticks_per_beat, self.tempo)

    @property
    def frequency(self) -> float:
        """Convert a MIDI note to frequency.

        Args:
        note: A MIDI note
        tuning: The tuning as defined by the frequency for A4.
        
        Returns:
            The frequency in Hertz of the note.
        """
        return (2 ** ((self.note_number - 69) / 12)) * self.tuning
    
    # def check(self) -> float:
    #     p: float = 1 / self.frequency
    #     n: float = self.duration_s / p

    def get_samples(self, rate: int) -> list[int]:
        duration: float = self.duration_s * 1000
        period: float = 1 / self.frequency
        waves: float = self.duration_s / period
        duration = math.floor(waves * period * 1000)
        # duration = math.floor(self.duration_s / (1 / self.frequency)) * 1000
        num_samples: int = math.floor(duration * (rate / 1000.0))
        frequency: float = self.frequency
        samples_float: list[float] = [1.0 * math.sin(2 * math.pi * frequency * ( x / rate )) for x in range(num_samples)]
        # samples_int: list[int] = [int(s * 32767) for s in samples_float]
        samples_int: list[int] = [32767 if s > 0 else -32768 for s in samples_float]
        return samples_int


class Rest(Note):
    def __init__(self, start: int, end: int, tempo: int = 500000, ticks_per_beat: int = 0) -> None:
        super().__init__(start, 0, tempo, ticks_per_beat)
        self.end = end
    
    def __repr__(self) -> str:
        return f'<taranislib.Rest {self.start}:{self.end}>'

    @property
    def note_number(self) -> int:
        return -1
    @note_number.setter
    def note_number(self, note_number: int) -> None:
        self._note_number = -1
    
    @property
    def frequency(self) -> int:
        """For a rest, always return 0 Hz.
        """
        return 0

    def get_samples(self, rate: int) -> list[int]:
        duration: float = mido.tick2second(self.duration, self.ticks_per_beat, self.tempo) * 1000
        num_samples: int = math.floor(duration * (rate / 1000.0))
        samples: list[int] = [0 for _ in range(num_samples)]
        return samples