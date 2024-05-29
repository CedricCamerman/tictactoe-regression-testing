import copy
from board_to_string_3p import string_to_board
from tictactoe_3p import ActionDomain, ResDom
import itertools

# five minute runtime
class ADS:
    def __init__(self):
        self.Q0 = '________________'
        self.TrA = {}

    def initialize_Q0(self):
        all_combinations = [''.join(combination) for combination in itertools.product('XO_', repeat=16)]
        return all_combinations

    def find_subsets(self):
        Qk = [self.Q0]
        self.TrA[self.Q0] = {'transitions': []}
        turn = 0 # 0 for user, 1 for computer1, 2 for computer2
        while True:
            Qj_plus_1 = []  # list of all states in Qj+1
            for A in Qk:
                for tile in range(16):
                    if A[tile] == '_':
                        successor, s_output = self.next_state(A, tile, turn)
                        if successor is not None:
                            if s_output == ResDom.PLAYING and successor not in Qj_plus_1: 
                                self.TrA[successor] = {'transitions': []}
                                Qj_plus_1.append(successor)
                            self.TrA[A]['transitions'].append((tile, turn, s_output, successor))
            if turn == 0:
                turn = 1
            elif turn == 1:
                turn = 2
            else:
                turn = 0

            if len(Qj_plus_1) == 0:
                break

            Qk = Qj_plus_1

    def next_state(self, board, tile, user_turn):
        sign = 'X' if user_turn == 0 else 'O' if user_turn == 1 else '/'
        successor = self.swap_character(board, tile, sign)
        result_state = self.get_result_state(successor)
        return successor, result_state

    def swap_character(self, s, index, new_char):
        if index < 0 or index >= len(s):
            raise ValueError("Index out of range")
        s_list = list(s)
        s_list[index] = new_char
        return ''.join(s_list)

    def check_winner(self, board, sign):
        # Check rows
        for row in range(4):
            for col in range(2):  # Only need to check starting points for rows
                if all(board[row * 4 + col + i] == sign for i in range(3)):
                    return True

        # Check columns
        for col in range(4):
            for row in range(2):  # Only need to check starting points for columns
                if all(board[(row + i) * 4 + col] == sign for i in range(3)):
                    return True

        # Check diagonals
        for row in range(2):
            for col in range(2):
                # Check diagonal from top-left to bottom-right
                if all(board[(row + i) * 4 + (col + i)] == sign for i in range(3)):
                    return True
                # Check diagonal from bottom-left to top-right
                if all(board[(row + 2 - i) * 4 + (col + i)] == sign for i in range(3)):
                    return True
        return False      
    
    def get_result_state(self, board):
        if self.check_winner(board, 'X'):
            return ResDom.U_WON
        elif self.check_winner(board, 'O'):
            return ResDom.C1_WON
        elif self.check_winner(board, '/'):
            return ResDom.C2_WON
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

ab = ADS()
ab.find_subsets()
# ab.display_metrics()
# # ab.run_test_case(TicTacToe())
