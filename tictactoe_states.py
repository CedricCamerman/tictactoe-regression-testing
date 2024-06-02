# Board tile states
from enum import Enum


class Sign(Enum):
    CROSS = 'X'
    NOUGHT = 'O'
    EMPTY = ' '

# Game states
class Status(Enum):
    TURN_USER = 1
    TURN_COMP = 2

# Actions
class ActionDomain(Enum):
    U_MOVE = 1
    C_MOVE = 2

# Result states
class ResDom(Enum):
    PLAYING = 1
    U_WON = 2
    C_WON = 3
    TIE = 4