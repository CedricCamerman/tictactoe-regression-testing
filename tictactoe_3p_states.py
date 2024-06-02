from enum import Enum

# Board tile states
class Sign(Enum):
    CROSS = 'X'
    NOUGHT = 'O'
    BAR = '/'
    EMPTY = ' '

# Game states
class Status(Enum):
    TURN_USER = 1
    TURN_COMP1 = 2
    TURN_COMP2 = 3

# Actions
class ActionDomain(Enum):
    U_MOVE = 1
    C1_MOVE = 2
    C2_MOVE = 3

# Result states
class ResDom(Enum):
    PLAYING = 1
    U_WON = 2
    C1_WON = 3
    C2_WON = 4
    TIE = 5