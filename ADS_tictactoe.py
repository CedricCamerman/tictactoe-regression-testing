from board_to_string import string_to_board
from tictactoe import ActionDomain, ResDom
import itertools

class ADS:
    def __init__(self):
        self.Q0 = '_________'
        self.TrA = {}

    def find_subsets(self):
        Qk = [self.Q0]
        self.TrA[self.Q0] = {'transitions': []}
        user_turn = True
        while True:
            Qj_plus_1 = []  # list of all states in Qj+1
            for A in Qk:
                for tile in range(9):
                    if A[tile] == '_':
                        successor, s_output = self.next_state(A, tile, user_turn)
                        if successor is not None:
                            if s_output == ResDom.PLAYING and successor not in Qj_plus_1: 
                                self.TrA[successor] = {'transitions': []}
                                Qj_plus_1.append(successor)
                            self.TrA[A]['transitions'].append((tile, user_turn, s_output, successor))
            if user_turn:
                user_turn = False
            else:
                user_turn = True

            if len(Qj_plus_1) == 0:
                break

            Qk = Qj_plus_1

    def next_state(self, board, tile, user_turn):
        successor = self.swap_character(board, tile, 'X' if user_turn else 'O')
        result_state = self.get_result_state(successor)
        return successor, result_state

    def swap_character(self, s, index, new_char):
        if index < 0 or index >= len(s):
            raise ValueError("Index out of range")
        s_list = list(s)
        s_list[index] = new_char
        return ''.join(s_list)

    def check_winner(self, board, sign):
        win_conditions = [
            [board[0], board[3], board[6]],
            [board[1], board[4], board[7]],
            [board[2], board[5], board[8]],
            [board[0], board[1], board[2]],
            [board[3], board[4], board[5]],
            [board[6], board[7], board[8]],
            [board[0], board[4], board[8]],
            [board[2], board[4], board[6]]
        ]
        return [sign, sign, sign] in win_conditions
    
    def get_result_state(self, board):
        if self.check_winner(board, 'X'):
            return ResDom.U_WON
        elif self.check_winner(board, 'O'):
            return ResDom.C_WON
        elif '_' not in board:
            return ResDom.TIE
        else:
            return ResDom.PLAYING
  

# ab = ADS()
# ab.find_subsets()
