import unittest
from tictactoe_3p import TicTacToe3P, Sign, Status, ResDom, ActionDomain

class TestTicTacToe3P(unittest.TestCase):
    # test tictactoe 3p board initialization
    def test_initialization(self):
        game = TicTacToe3P()
        self.assertEqual(game.status, Status.TURN_USER)
        self.assertEqual(game.res, ResDom.PLAYING)
        self.assertEqual(game.numOfMoves, 0)
    
    # test winning on a row
    def test_win_on_row(self):
        game = TicTacToe3P()
        game.board = [[Sign.EMPTY, Sign.EMPTY, Sign.EMPTY, Sign.EMPTY],
                      [Sign.EMPTY, Sign.EMPTY, Sign.EMPTY, Sign.EMPTY],
                      [Sign.EMPTY, Sign.EMPTY, Sign.EMPTY, Sign.EMPTY],
                      [Sign.CROSS, Sign.CROSS, Sign.CROSS, Sign.EMPTY]]
        self.assertTrue(game.winOnRow(3, 0, Sign.CROSS))
        self.assertFalse(game.winOnRow(3, 0, Sign.NOUGHT))
    
    # test winning on a column
    def test_win_on_col(self):
        game = TicTacToe3P()
        game.board = [[Sign.CROSS, Sign.EMPTY, Sign.EMPTY, Sign.EMPTY],
                      [Sign.CROSS, Sign.EMPTY, Sign.EMPTY, Sign.EMPTY],
                      [Sign.CROSS, Sign.EMPTY, Sign.EMPTY, Sign.EMPTY],
                      [Sign.EMPTY, Sign.EMPTY, Sign.EMPTY, Sign.EMPTY]]
        self.assertTrue(game.winOnCol(0, 0, Sign.CROSS))
        self.assertFalse(game.winOnCol(0, 0, Sign.NOUGHT))

    # test winning on a diagonal
    def test_win_on_diag(self):
        game = TicTacToe3P()
        game.board = [[Sign.CROSS, Sign.EMPTY, Sign.EMPTY, Sign.EMPTY],
                      [Sign.EMPTY, Sign.CROSS, Sign.EMPTY, Sign.EMPTY],
                      [Sign.EMPTY, Sign.EMPTY, Sign.CROSS, Sign.EMPTY],
                      [Sign.EMPTY, Sign.EMPTY, Sign.EMPTY, Sign.EMPTY]]
        self.assertTrue(game.winOnDiag(0, 0, Sign.CROSS))
    
    # test winning on a diagonal opposite
    def test_win_on_diag_opposite(self):
        game = TicTacToe3P()
        game.board = [[Sign.EMPTY, Sign.EMPTY, Sign.EMPTY, Sign.EMPTY],
                      [Sign.EMPTY, Sign.EMPTY, Sign.CROSS, Sign.EMPTY],
                      [Sign.EMPTY, Sign.CROSS, Sign.EMPTY, Sign.EMPTY],
                      [Sign.CROSS, Sign.EMPTY, Sign.EMPTY, Sign.EMPTY]]
        self.assertTrue(game.winOnDiag(3, 0, Sign.CROSS))

    # test tie
    def test_tie(self):
        game = TicTacToe3P()
        game.board = [[Sign.EMPTY, Sign.NOUGHT, Sign.CROSS, Sign.BAR],
                      [Sign.CROSS, Sign.NOUGHT, Sign.CROSS, Sign.CROSS],
                      [Sign.NOUGHT, Sign.BAR, Sign.BAR, Sign.NOUGHT],
                      [Sign.CROSS, Sign.NOUGHT, Sign.CROSS, Sign.BAR]]
        game.numOfMoves = 15
        game.uSelRow = 0
        game.uSelCol = 0
        game.action = ActionDomain.U_MOVE
        game.main()
        self.assertEqual(game.res, ResDom.TIE)

    # test user win
    def test_user_win(self):
        game = TicTacToe3P()
        game.board = [[Sign.EMPTY, Sign.CROSS, Sign.CROSS, Sign.CROSS],
                      [Sign.CROSS, Sign.NOUGHT, Sign.NOUGHT, Sign.NOUGHT],
                      [Sign.NOUGHT, Sign.CROSS, Sign.NOUGHT, Sign.NOUGHT],
                      [Sign.NOUGHT, Sign.CROSS, Sign.NOUGHT, Sign.NOUGHT]]
        game.numOfMoves = 16
        game.uSelRow = 0
        game.uSelCol = 0
        game.action = ActionDomain.U_MOVE
        game.main()
        self.assertEqual(game.res, ResDom.U_WON)

    # test computer 1 win
    def test_comp1_win(self):
        game = TicTacToe3P()
        game.board = [[Sign.EMPTY, Sign.CROSS, Sign.BAR, Sign.CROSS],
                      [Sign.CROSS, Sign.NOUGHT, Sign.BAR, Sign.NOUGHT],
                      [Sign.NOUGHT, Sign.CROSS, Sign.NOUGHT, Sign.BAR],
                      [Sign.NOUGHT, Sign.CROSS, Sign.NOUGHT, Sign.BAR]]
        game.action = ActionDomain.C1_MOVE
        game.status = Status.TURN_COMP1
        game.main()
        self.assertEqual(game.res, ResDom.C1_WON)

    # test computer 2 win
    def test_comp2_win(self):
        game = TicTacToe3P()
        game.board = [[Sign.EMPTY, Sign.BAR, Sign.BAR, Sign.CROSS],
                      [Sign.CROSS, Sign.NOUGHT, Sign.BAR, Sign.NOUGHT],
                      [Sign.NOUGHT, Sign.CROSS, Sign.NOUGHT, Sign.BAR],
                      [Sign.NOUGHT, Sign.CROSS, Sign.NOUGHT, Sign.BAR]]
        game.action = ActionDomain.C2_MOVE
        game.status = Status.TURN_COMP2
        game.main()
        self.assertEqual(game.res, ResDom.C2_WON)

    # test invalid user move
    def test_invalid_user_move(self):
        game = TicTacToe3P()
        game.board = [[Sign.NOUGHT, Sign.EMPTY, Sign.EMPTY, Sign.EMPTY],
                      [Sign.BAR, Sign.CROSS, Sign.EMPTY, Sign.EMPTY],
                      [Sign.NOUGHT, Sign.NOUGHT, Sign.EMPTY, Sign.EMPTY],
                      [Sign.NOUGHT, Sign.NOUGHT, Sign.EMPTY, Sign.EMPTY]]
        game.uSelRow = 1
        game.uSelCol = 0
        game.action = ActionDomain.U_MOVE
        game.main()
        self.assertEqual(game.status, Status.TURN_USER)

if __name__ == '__main__':
    unittest.main()
