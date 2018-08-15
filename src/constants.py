from enum import Enum

class Segment(Enum):
    Jeopardy = 1
    DoubleJeopardy = 2
    FinalJeopardy = 3

class ProgramMode(Enum):
    Empty = 1
    Neutral = 2
    Editing = 3
    Playing = 4

class DisplayType(Enum):
    Category = 1
    Clue = 2

class DisplayState(Enum):
    Blank = 1
    Waiting = 2
    Category = 3
    Explanation = 4
    Clue = 5
    Response = 6
    Dollars = 7
    Points = 8
    Emblem = 9



