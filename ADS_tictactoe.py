import copy
from board_to_string import string_to_board
from tictactoe import ActionDomain, ResDom
import itertools

class ADS:
    def __init__(self):
        self.Q0 = '_________'
        self.TrA = {}

    def initialize_Q0(self):
        all_combinations = [''.join(combination) for combination in itertools.product('XO_', repeat=9)]
        return all_combinations

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
  
    def display_metrics(self):
        num_states = len(self.P)
        num_transitions = sum(len(self.P[state]['transitions']) for state in self.P.keys())
        output_complete = all(
            all(output in {trans[1] for trans in self.P[state]['transitions']} for output in ResDom)
            for state in self.P.keys() if len(self.P[state]['transitions']) > 0
        )
        print(f"Number of states in P: {num_states}")
        print(f"Number of transitions in P: {num_transitions}")
        print(f"Is output-complete: {output_complete}")

    def run_test_case(self, tictactoe_game):
        correct_count = 0
        incorrect_count = 0
        for state in self.P.keys():
            for (move, expected_output, next_state) in self.P[state]['transitions']:
                tictactoe_game.board = copy.deepcopy(string_to_board(state))
                tictactoe_game.uSelRow, tictactoe_game.uSelCol = move
                tictactoe_game.main()
                if tictactoe_game.res == ResDom.PLAYING:
                    tictactoe_game.action = ActionDomain.C_MOVE
                    tictactoe_game.main()
                if tictactoe_game.res != expected_output:
                    incorrect_count += 1
                    print(f"Test failed for move {move} from state {state}. Expected {expected_output}, got {tictactoe_game.res}")
                else:
                    correct_count += 1
                    print(f"Test passed for move {move} from state {state}. Expected {expected_output}, got {tictactoe_game.res}")
        
        total_tests = correct_count + incorrect_count
        accuracy = correct_count / total_tests if total_tests > 0 else 0

        print(f"Total tests run: {total_tests}")
        print(f"Correct outputs: {correct_count}")
        print(f"Incorrect outputs: {incorrect_count}")
        print(f"Accuracy: {accuracy * 100:.2f}%")

# ab = ADS()
# ab.find_subsets()
# ab.display_metrics()
# # ab.run_test_case(TicTacToe())
