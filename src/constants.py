from enum import Enum

class Segment(Enum):
    Jeopardy = 1
    DoubleJeopardy = 2
    FinalJeopardy = 3

class ProgramState(Enum):
    Neutral = 1
    Editing = 2
    Playing = 3

