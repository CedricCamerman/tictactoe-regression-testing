from tictactoe_ultimate import ActionDomain, ResDom
import itertools
import time

class ADS:
    def __init__(self):
        self.Q0 = '_________'
        # self.P0 is a 3x3 matrix of ResDom.PLAYING (in string form)
        self.P0 = '_________'
        self.TrA = {}
        self.TrB = {}

    def initialize_Q0(self):
        all_combinations = [''.join(combination) for combination in itertools.product('XO_', repeat=9)]
        return all_combinations

    def find_subsets(self):
        start_time = time.time()
        Qk = [self.Q0]
        self.TrA[self.Q0] = {'transitions': []}
        while True:
            Qj_plus_1 = []  # list of all states in Qj+1
            for A in Qk:
                for tile in range(9):
                    if A[tile] == '_':
                        for user_turn in [True, False]:
                            successor, s_output = self.next_state(A, tile, user_turn)
                            if successor is not None:
                                if s_output == ResDom.PLAYING and successor not in Qj_plus_1: 
                                    self.TrA[successor] = {'transitions': []}
                                    Qj_plus_1.append(successor)
                                self.TrA[A]['transitions'].append((tile, s_output, successor))
            if len(Qj_plus_1) == 0:
                break

            Qk = Qj_plus_1
        
        # Transitions of smaller boards complete. Now we need to find transitions for the larger board           
        Pk = [self.P0]
        self.TrB[self.P0] = {'transitions': [(ResDom.PLAYING, self.P0)]}
        while True:
            Pj_plus_1 = []  # list of all states in Qj+1
            for B in Pk:
                for tile in range(9):
                    if B[tile] == '_':
                        # for res_type in [ResDom.U_WON, ResDom.C_WON]:
                        for res_type in [ResDom.U_WON, ResDom.C_WON, ResDom.TIE]:
                            successor, s_output = self.next_state_board(B, tile, res_type)
                            if successor is not None:
                                if s_output == ResDom.PLAYING and successor not in Pj_plus_1: 
                                    self.TrB[successor] = {'transitions': [(s_output, successor)]}
                                    Pj_plus_1.append(successor)
                                self.TrB[B]['transitions'].append((s_output, successor))
            if len(Pj_plus_1) == 0:
                print(f"Time taken: {time.time() - start_time}")
                break

            Pk = Pj_plus_1

    def next_state(self, board, tile, user_turn):
        successor = self.swap_character(board, tile, 'X' if user_turn else 'O')
        result_state = self.get_result_state(successor)
        return successor, result_state
    
    def next_state_board(self, board, tile, res_type):
        if res_type == ResDom.U_WON:
            char = 'X'
        elif res_type == ResDom.C_WON:
            char = 'O'
        else:
            char = '-'
        successor = self.swap_character(board, tile, char)
        result_state = self.get_result_state_board(successor)
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
        
    def get_result_state_board(self, board):
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
