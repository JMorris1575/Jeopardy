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
    A_Text = 3
    B_Text = 4
    Dollars = 5
    Points = 6
    SegmentCard = 7
    DailyDouble = 8

class PlayMode(Enum):
    StartGame = 1
    RevealCategories = 2
    SelectClue = 3




