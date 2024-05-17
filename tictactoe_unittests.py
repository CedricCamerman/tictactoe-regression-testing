# import libraries for unit tests
import unittest
from tictactoe import ActionDomain, ResDom, Sign, Status, TicTacToe

# create a test class
class TestTicTacToe(unittest.TestCase):
    # test tictactoe board initialization
    def test_initialization(self):
        game = TicTacToe()
        self.assertEqual(game.status, Status.TURN_USER)
        self.assertEqual(game.res, ResDom.PLAYING)
        self.assertEqual(game.numOfMoves, 0)
    
    # test winning on a row
    def test_win_on_row(self):
        game = TicTacToe()
        game.board = [[Sign.CROSS, Sign.CROSS, Sign.CROSS],
                      [Sign.EMPTY, Sign.EMPTY, Sign.EMPTY],
                      [Sign.EMPTY, Sign.EMPTY, Sign.EMPTY]]
        self.assertTrue(game.winOnRow(0, 0, Sign.CROSS))
        self.assertFalse(game.winOnRow(0, 0, Sign.NOUGHT))
    
    # test winning on a column
    def test_win_on_col(self):
        game = TicTacToe()
        game.board = [[Sign.CROSS, Sign.EMPTY, Sign.EMPTY],
                      [Sign.CROSS, Sign.EMPTY, Sign.EMPTY],
                      [Sign.CROSS, Sign.EMPTY, Sign.EMPTY]]
        self.assertTrue(game.winOnCol(0, 0, Sign.CROSS))
        self.assertFalse(game.winOnCol(0, 0, Sign.NOUGHT))

    # test winning on a diagonal
    def test_win_on_diag(self):
        game = TicTacToe()
        game.board = [[Sign.CROSS, Sign.EMPTY, Sign.EMPTY],
                      [Sign.EMPTY, Sign.CROSS, Sign.EMPTY],
                      [Sign.EMPTY, Sign.EMPTY, Sign.CROSS]]
        self.assertTrue(game.winOnDiag(0, 0, Sign.CROSS))

    # test winning on a diagonal opposite
    def test_win_on_diag_opposite(self):
        game = TicTacToe()
        game.board = [[Sign.EMPTY, Sign.EMPTY, Sign.CROSS],
                      [Sign.EMPTY, Sign.CROSS, Sign.EMPTY],
                      [Sign.CROSS, Sign.EMPTY, Sign.EMPTY]]
        self.assertTrue(game.winOnDiag(2, 0, Sign.CROSS))

    # test tie
    def test_tie(self):
        game = TicTacToe()
        game.board = [[Sign.EMPTY, Sign.NOUGHT, Sign.CROSS],
                      [Sign.CROSS, Sign.NOUGHT, Sign.CROSS],
                      [Sign.NOUGHT, Sign.CROSS, Sign.NOUGHT]]
        game.numOfMoves = 8
        game.uSelRow = 0
        game.uSelCol = 0
        game.action = ActionDomain.U_MOVE
        game.main()
        self.assertEqual(game.res, ResDom.TIE)

    # test user win
    def test_user_win(self):
        game = TicTacToe()
        game.board = [[Sign.EMPTY, Sign.CROSS, Sign.CROSS],
                      [Sign.CROSS, Sign.NOUGHT, Sign.NOUGHT],
                      [Sign.NOUGHT, Sign.CROSS, Sign.NOUGHT]]
        game.numOfMoves = 8
        game.uSelRow = 0
        game.uSelCol = 0
        game.action = ActionDomain.U_MOVE
        game.status = Status.TURN_USER
        game.main()
        self.assertEqual(game.res, ResDom.U_WON)

    # test cpu win
    def test_cpu_win(self):
        game = TicTacToe()
        game.board = [[Sign.EMPTY, Sign.NOUGHT, Sign.CROSS],
                      [Sign.CROSS, Sign.NOUGHT, Sign.CROSS],
                      [Sign.NOUGHT, Sign.CROSS, Sign.NOUGHT]]
        game.numOfMoves = 8
        game.action = ActionDomain.C_MOVE
        game.status = Status.TURN_COMP
        game.main()
        self.assertEqual(game.res, ResDom.C_WON)
    
    # test making a move
    def test_make_move(self):
        game = TicTacToe()
        game.makeMove(0, 0, Sign.CROSS)
        self.assertEqual(game.board[0][0], Sign.CROSS)
        self.assertEqual(game.numOfMoves, 1)
        self.assertEqual(game.res, ResDom.PLAYING)
    
    # test user move
    def test_user_move(self):
        game = TicTacToe()
        game.uSelRow = 0
        game.uSelCol = 0
        game.action = ActionDomain.U_MOVE
        game.main()
        self.assertEqual(game.board[0][0], Sign.CROSS)
        self.assertEqual(game.status, Status.TURN_COMP)
        self.assertEqual(game.numOfMoves, 1)
        self.assertEqual(game.res, ResDom.PLAYING)

    # test invalid user move
    def test_invalid_user_move(self):
        game = TicTacToe()
        game.board = [[Sign.EMPTY, Sign.NOUGHT, Sign.CROSS],
                      [Sign.CROSS, Sign.NOUGHT, Sign.CROSS],
                      [Sign.NOUGHT, Sign.CROSS, Sign.NOUGHT]]
        game.uSelRow = 0
        game.uSelCol = 1
        game.numOfMoves = 8
        game.action = ActionDomain.U_MOVE
        game.status = Status.TURN_USER
        game.main()
        self.assertEqual(game.board[0][1], Sign.NOUGHT)
        self.assertEqual(game.status, Status.TURN_USER)
        self.assertEqual(game.numOfMoves, 8)
        self.assertEqual(game.res, ResDom.PLAYING)
    
    # test non-deterministic cpu move (randomised) and solve oracle problem
    def test_cpu_move(self):
        game = TicTacToe()
        game.board = [[Sign.CROSS, Sign.NOUGHT, Sign.CROSS],
                      [Sign.CROSS, Sign.EMPTY, Sign.CROSS],
                      [Sign.NOUGHT, Sign.CROSS, Sign.NOUGHT]]
        game.status = Status.TURN_COMP
        game.action = ActionDomain.C_MOVE
        game.numOfMoves = 8
        game.main()
        self.assertEqual(game.board[1][1], Sign.NOUGHT)
        self.assertEqual(game.status, Status.TURN_USER)
        self.assertEqual(game.numOfMoves, 9)
        self.assertEqual(game.res, ResDom.TIE)

# run the tests
if __name__ == '__main__':
    unittest.main()

# run the tests with coverage
# coverage run -m unittest tictactoe_unittests.py


