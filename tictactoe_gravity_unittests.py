# imports
import unittest
from tictactoe_gravity_states import Sign, Status, ActionDomain, ResDom
from tictactoe_gravity import TicTacToeGravity


class TestTicTacToeGravity(unittest.TestCase):
    # test tictactoe gravity board initialization
    def test_initialization(self):
        game = TicTacToeGravity()
        self.assertEqual(game.status, Status.TURN_USER)
        self.assertEqual(game.res, ResDom.PLAYING)
        self.assertEqual(game.numOfMoves, 0)
    
    # test winning on a row
    def test_win_on_row(self):
        game = TicTacToeGravity()
        game.board = [[Sign.EMPTY, Sign.EMPTY, Sign.EMPTY],
                      [Sign.EMPTY, Sign.EMPTY, Sign.EMPTY],
                      [Sign.CROSS, Sign.CROSS, Sign.CROSS]]
        self.assertTrue(game.winOnRow(2, 0, Sign.CROSS))
        self.assertFalse(game.winOnRow(2, 0, Sign.NOUGHT))
    
    # test winning on a column
    def test_win_on_col(self):
        game = TicTacToeGravity()
        game.board = [[Sign.CROSS, Sign.EMPTY, Sign.EMPTY],
                      [Sign.CROSS, Sign.EMPTY, Sign.EMPTY],
                      [Sign.CROSS, Sign.EMPTY, Sign.EMPTY]]
        self.assertTrue(game.winOnCol(0, 0, Sign.CROSS))
        self.assertFalse(game.winOnCol(0, 0, Sign.NOUGHT))

    # test winning on a diagonal
    def test_win_on_diag(self):
        game = TicTacToeGravity()
        game.board = [[Sign.CROSS, Sign.EMPTY, Sign.EMPTY],
                      [Sign.NOUGHT, Sign.CROSS, Sign.EMPTY],
                      [Sign.NOUGHT, Sign.NOUGHT, Sign.CROSS]]
        self.assertTrue(game.winOnDiag(0, 0, Sign.CROSS))

    # test winning on a diagonal opposite
    def test_win_on_diag_opposite(self):
        game = TicTacToeGravity()
        game.board = [[Sign.EMPTY, Sign.EMPTY, Sign.CROSS],
                      [Sign.EMPTY, Sign.CROSS, Sign.NOUGHT],
                      [Sign.CROSS, Sign.NOUGHT, Sign.NOUGHT]]
        self.assertTrue(game.winOnDiag(2, 0, Sign.CROSS))

    # test tie
    def test_tie(self):
        game = TicTacToeGravity()
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
        game = TicTacToeGravity()
        game.board = [[Sign.EMPTY, Sign.NOUGHT, Sign.CROSS],
                      [Sign.EMPTY, Sign.NOUGHT, Sign.NOUGHT],
                      [Sign.EMPTY, Sign.CROSS, Sign.CROSS]]
        game.uSelRow = 0
        game.uSelCol = 0
        game.action = ActionDomain.U_MOVE
        game.main()
        self.assertEqual(game.res, ResDom.U_WON)

    # test computer win
    def test_comp_win(self):
        game = TicTacToeGravity()
        game.board = [[Sign.NOUGHT, Sign.CROSS, Sign.EMPTY],
                      [Sign.CROSS, Sign.NOUGHT, Sign.EMPTY],
                      [Sign.CROSS, Sign.NOUGHT, Sign.EMPTY]]
        game.action = ActionDomain.C_MOVE
        game.status = Status.TURN_COMP
        game.main()
        self.assertEqual(game.res, ResDom.C_WON)

    # test makeMove column full
    def test_makeMove_column_full(self):
        game = TicTacToeGravity()
        game.board = [[Sign.NOUGHT, Sign.NOUGHT, Sign.EMPTY],
                      [Sign.CROSS, Sign.CROSS, Sign.EMPTY],
                      [Sign.NOUGHT, Sign.NOUGHT, Sign.EMPTY]]
        game.uSelRow = 0
        game.uSelCol = 0
        game.action = ActionDomain.U_MOVE
        self.assertFalse(game.makeMove(0, 0, Sign.CROSS))

    # test moveUser occupied cell
    def test_moveUser_occupied_cell(self):
        game = TicTacToeGravity()
        game.board = [[Sign.NOUGHT, Sign.EMPTY, Sign.EMPTY],
                      [Sign.CROSS, Sign.CROSS, Sign.EMPTY],
                      [Sign.NOUGHT, Sign.NOUGHT, Sign.EMPTY]]
        game.uSelRow = 1
        game.uSelCol = 1
        game.action = ActionDomain.U_MOVE
        game.main()
        self.assertEqual(game.status, Status.TURN_USER)


if __name__ == '__main__':
    unittest.main()

