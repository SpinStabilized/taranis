# -*- coding: utf-8 -*-
import mido

class TaranisMessage:
    def __init__(self, message: mido.Message):
        self.message:mido.Message = message
        self.tick: int = 0
    
    def __repr__(self) -> str:
        return f'<taranislib.Message {self.type}@{self.tick}'

    @property
    def note(self) -> int:
        return self.message.dict()['note']

    @property
    def type(self) -> str:
        return self.message.dict()['type']

    @property
    def time(self) -> int:
        return self.message.dict()['time']

    @property
    def velocity(self) -> int:
        return self.message.dict()['velocity']

    @property
    def is_control(self) -> bool:
        return self.message.dict()['type'] not in ['note_on', 'note_off']
    
    @property
    def is_note(self) -> bool:
        return self.message.dict()['type'] in ['note_on', 'note_off']
