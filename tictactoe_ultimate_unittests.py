# import ultimate tictactoe unittests
import unittest
from tictactoe_ultimate import UltimateTicTacToe
from tictactoe import Sign, Status, ActionDomain, ResDom


class TestUltimateTicTacToe(unittest.TestCase):
    # test ultimate tictactoe board initialization
    def test_initialization(self):
        game = UltimateTicTacToe()
        self.assertEqual(game.status, Status.TURN_USER)
        self.assertEqual(game.res, ResDom.PLAYING)
        self.assertEqual(game.numOfMoves, 0)

    # test winning on a row
    def test_win_on_row(self):
        game = UltimateTicTacToe()
        # generate 9 regular boards where the user wins in board 7, 8 and 9
        for i in range(3):
            game.board[2][i].res = ResDom.U_WON
        self.assertTrue(game.winOnRow(2, 0, Sign.CROSS))
        self.assertFalse(game.winOnRow(2, 0, Sign.NOUGHT))

    # test winning on a column
    def test_win_on_col(self):
        game = UltimateTicTacToe()
        # generate 9 regular boards where the user wins in board 1, 4 and 7
        for i in range(3):
            game.board[i][0].res = ResDom.U_WON
        self.assertTrue(game.winOnCol(0, 0, Sign.CROSS))
        self.assertFalse(game.winOnCol(0, 0, Sign.NOUGHT))

    # test winning on a diagonal
    def test_win_on_diag(self):
        game = UltimateTicTacToe()
        # generate 9 regular boards where the user wins in board 1, 5 and 9
        for i in range(3):
            game.board[i][i].res = ResDom.U_WON
        self.assertTrue(game.winOnDiag(0, 0, Sign.CROSS))

    # test winning on a diagonal opposite
    def test_win_on_diag_opposite(self):
        game = UltimateTicTacToe()
        # generate 9 regular boards where the user wins in board 3, 5 and 7
        for i in range(3):
            game.board[i][2 - i].res = ResDom.U_WON
        self.assertTrue(game.winOnDiag(2, 0, Sign.CROSS))

    # test tie
    def test_tie(self):
        game = UltimateTicTacToe()
        # generate 9 regular boards where the game ends in a tie
        for i in range(3):
            for j in range(3):
                game.board[i][j].res = ResDom.TIE
        game.board[0][0].res = ResDom.PLAYING
        game.board[0][0].board = [[Sign.CROSS, Sign.NOUGHT, Sign.CROSS],
                                  [Sign.NOUGHT, Sign.EMPTY, Sign.NOUGHT],
                                  [Sign.CROSS, Sign.NOUGHT, Sign.CROSS]]
        game.numOfMoves = 80
        game.uSelBoardcol = 0
        game.uSelBoardrow = 0
        game.uSelRow = 1
        game.uSelCol = 1
        game.main()
        self.assertEqual(game.res, ResDom.TIE)

    # test user win
    def test_user_win(self):
        game = UltimateTicTacToe()
        # generate 9 regular boards where the user wins in board 1, 5 and 9
        for i in range(2):
            game.board[i][i].res = ResDom.U_WON
        game.board[2][2].board = [[Sign.CROSS, Sign.EMPTY, Sign.CROSS],
                                  [Sign.NOUGHT, Sign.EMPTY, Sign.NOUGHT],
                                  [Sign.CROSS, Sign.NOUGHT, Sign.CROSS]]
        game.makeMove(2, 2, 0, 1, Sign.CROSS)
        game.uSelBoardrow = 0
        game.uSelBoardcol = 1
        game.uSelRow = 1
        game.uSelCol = 1
        game.main()
        self.assertEqual(game.res, ResDom.U_WON)

    # test computer win
    def test_comp_win(self):
        game = UltimateTicTacToe()
        # generate 9 regular boards where the computer wins in board 1, 5 and 9
        for i in range(3):
            for j in range(3):
                game.board[i][j].res = ResDom.TIE
        for i in range(2):
            game.board[i][0].res = ResDom.C_WON
        game.board[2][0].res = ResDom.PLAYING
        game.board[2][0].board = [[Sign.CROSS, Sign.NOUGHT, Sign.CROSS],
                                   [Sign.NOUGHT, Sign.EMPTY, Sign.NOUGHT],
                                   [Sign.CROSS, Sign.NOUGHT, Sign.CROSS]]
        game.status = Status.TURN_COMP
        game.action = ActionDomain.C_MOVE
        game.main()
        self.assertEqual(game.res, ResDom.C_WON)
    
    # test making a move
    def test_make_move(self):
        game = UltimateTicTacToe()
        game.makeMove(0, 0, 0, 0, Sign.CROSS)
        self.assertEqual(game.board[0][0].board[0][0], Sign.CROSS)
        self.assertEqual(game.numOfMoves, 1)
        self.assertEqual(game.res, ResDom.PLAYING)

    # test win on diag for cpu
    def test_win_on_diag_cpu(self):
        game = UltimateTicTacToe()
        # generate 9 regular boards where the computer wins in board 1, 5 and 9
        for i in range(3):
            for j in range(3):
                game.board[i][j].res = ResDom.TIE
        for i in range(2):
            game.board[i][i].res = ResDom.C_WON
        game.board[2][2].res = ResDom.PLAYING
        game.board[2][2].board = [[Sign.CROSS, Sign.NOUGHT, Sign.CROSS],
                                  [Sign.NOUGHT, Sign.EMPTY, Sign.NOUGHT],
                                  [Sign.CROSS, Sign.NOUGHT, Sign.CROSS]]
        game.status = Status.TURN_COMP
        game.action = ActionDomain.C_MOVE
        game.main()
        self.assertEqual(game.res, ResDom.C_WON)
    
    # test win on diag for cpu reverse
    def test_win_on_diag_cpu_reverse(self):
        game = UltimateTicTacToe()
        # generate 9 regular boards where the computer wins in board 3, 5 and 7
        for i in range(3):
            for j in range(3):
                game.board[i][j].res = ResDom.TIE
        for i in range(2):
            game.board[i][2 - i].res = ResDom.C_WON
        game.board[2][0].res = ResDom.PLAYING
        game.board[2][0].board = [[Sign.CROSS, Sign.NOUGHT, Sign.CROSS],
                                  [Sign.NOUGHT, Sign.EMPTY, Sign.NOUGHT],
                                  [Sign.CROSS, Sign.NOUGHT, Sign.CROSS]]
        game.status = Status.TURN_COMP
        game.action = ActionDomain.C_MOVE
        game.main()
        self.assertEqual(game.res, ResDom.C_WON)
    
    # test cpu non winning move
    def test_cpu_non_winning_move(self):
        game = UltimateTicTacToe()
        game.status = Status.TURN_COMP
        game.action = ActionDomain.C_MOVE
        game.main()
        self.assertEqual(game.res, ResDom.PLAYING)

    # test invalid move
    def test_invalid_move(self):
        game = UltimateTicTacToe()
        game.board[0][0].board[0][0] = Sign.CROSS
        game.uSelBoardcol = 0
        game.uSelBoardrow = 0
        game.uSelRow = 0
        game.uSelCol = 0
        game.action = ActionDomain.U_MOVE
        game.main()
        self.assertEqual(game.status, Status.TURN_USER)


if __name__ == '__main__':
    unittest.main()