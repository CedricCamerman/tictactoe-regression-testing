import time
import unittest
from tictactoe import ActionDomain, ResDom, Sign, Status, TicTacToe
from enum import Enum
import random

class TestTicTacToe(unittest.TestCase):
    def test_initialization(self):
        game = TicTacToe()
        self.assertEqual(game.status, Status.TURN_USER)
        self.assertEqual(game.res, ResDom.PLAYING)
        self.assertEqual(game.numOfMoves, 0)
        # Add more assertions as needed

    def test_user_move(self):
        game = TicTacToe()
        game.uSelRow = 0
        game.uSelCol = 0
        game.action = ActionDomain.U_MOVE
        game.main()
        self.assertEqual(game.board[0][0], Sign.CROSS)
        # Add more assertions as needed

    # Add more test methods for other components of your program

test = TestTicTacToe()
test.test_initialization()
test.test_user_move()
