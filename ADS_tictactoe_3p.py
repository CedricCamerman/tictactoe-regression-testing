import copy
from board_to_string_3p import string_to_board
from tictactoe_3p import ActionDomain, ResDom
import itertools
import time
import random

# five minute runtime
class ADS:
    def __init__(self):
        self.Q0 = '________________'
        self.TrA_trails = {}
        self.TrA = {}
        self.keylist = [] # keep a spare list of boards that have the selected amount of empty tiles for efficiency in MCT

    def initialize_Q0(self):
        all_combinations = [''.join(combination) for combination in itertools.product('XO_', repeat=16)]
        return all_combinations

    def find_subsets(self):
        start_time = time.time()
        # end_time = start_time + 5 * 60

        # Step 1: Initialize Q
        Q_init = [self.Q0]
        self.TrA_trails[self.Q0] = {'transitions': []}
        turn = 0 # 0 for user, 1 for computer1, 2 for computer2
        while True:
            Qj_plus_1 = []  # list of all states in Qj+1
            # Initial transitions
            for A in Q_init:
                for tile in range(16):
                    if A[tile] == '_':
                        successor, s_output = self.next_state(A, tile, turn)
                        if successor is not None:
                            if s_output == ResDom.PLAYING and successor not in Qj_plus_1: 
                                self.TrA_trails[successor] = {'transitions': []}
                                Qj_plus_1.append(successor)
                            self.TrA_trails[A]['transitions'].append((tile, turn, s_output, successor))
            Q_init = Qj_plus_1
            turn = 1
            break

        # Step 2: Monte Carlo depth-first trails
        Qk = Q_init
        while True:
            Qj_plus_1 = [] # list of all states in Qj+1. All further successors will be temporarily ignored
            for A in Qk:
                # simulate A fully and randomly, and record all transitions. Put first successor in Qj+1.
                # Choose a random empty tile in A using the random library
                temp_turn = turn
                current_state = A
                current_state_results = ResDom.PLAYING
                empty_tiles = [i for i in range(16) if A[i] == '_']
                while current_state_results == ResDom.PLAYING:
                    random_tile = random.choice(empty_tiles)
                    successor, s_output = self.next_state(current_state, random_tile, temp_turn)
                    if successor is not None:
                            if s_output == ResDom.PLAYING and successor not in Qj_plus_1: 
                                self.TrA_trails[successor] = {'transitions': []}
                                if current_state == A:
                                    Qj_plus_1.append(successor)
                            if (random_tile, temp_turn, s_output, successor) not in self.TrA_trails[A]['transitions']:
                                self.TrA_trails[current_state]['transitions'].append((random_tile, temp_turn, s_output, successor))
                    current_state = successor
                    current_state_results = s_output
                    empty_tiles = [i for i in range(16) if successor[i] == '_']
                    if temp_turn == 0:
                        temp_turn = 1
                    elif temp_turn == 1:
                        temp_turn = 2
                    else:
                        temp_turn = 0

            if turn == 0:
                turn = 1
            elif turn == 1:
                turn = 2
            else:
                turn = 0

            if len(Qj_plus_1) == 0:
                break

            Qk = Qj_plus_1

        # Step 3: Track back from the end states to the initial state and search breadth first
        # Ql is the tuplelist of all states that are not right before the end states (board, [list of inputs already done])
        E = 7 # empty tiles cutoff
        Ql = [] 
        empty_tiles_amount = 2 # start
        turn = 2 # turn starts out with two empty tiles so cpu2 goes first
        Qk = Ql
        while True:
            user_turn = turn
            Qk = []
            # find all keys in TrA with empty_tiles_amount empty tiles
            for key in self.TrA_trails.keys():
                if key.count('_') == empty_tiles_amount:
                    self.TrA[key] = {'transitions': []}
                    if empty_tiles_amount == E:
                        self.keylist.append(key)
                    Qk.append(key)
            # regular simulations
            while True:
                Qj_plus_1 = []  # list of all states in Qj+1
                for A in Qk:
                    for tile in range(16):
                        if A[tile] == '_':
                            successor, s_output = self.next_state(A, tile, user_turn)
                            if successor is not None:
                                if s_output == ResDom.PLAYING:
                                    if successor not in Qj_plus_1:
                                        Qj_plus_1.append(successor)
                                        if successor not in self.TrA.keys(): 
                                            self.TrA[successor] = {'transitions': []}
                                if (tile, user_turn, s_output, successor) not in self.TrA[A]['transitions']:
                                    self.TrA[A]['transitions'].append((tile, user_turn, s_output, successor))
                if user_turn == 0:
                    user_turn = 1
                elif user_turn == 1:
                    user_turn = 2
                else:
                    user_turn = 0

                if len(Qj_plus_1) == 0:
                    break

                Qk = Qj_plus_1

            
            if empty_tiles_amount == E:
                print(f"ADS generation time for {E} empty_tiles, ADS length of {len(self.TrA)}, time of {time.time() - start_time}")
                break
            empty_tiles_amount += 1
            if turn == 0:
                    turn = 2
            elif turn == 1:
                turn = 0
            else:
                turn = 1
            
            

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
        # Top-left to bottom-right
        if (board[1] == sign and board[6] == sign and board[11] == sign) or \
           (board[0] == sign and board[5] == sign and board[10] == sign) or \
           (board[5] == sign and board[10] == sign and board[15] == sign) or \
           (board[4] == sign and board[9] == sign and board[14] == sign):
            return True  
        # Bottom-left to top-right
        if (board[8] == sign and board[5] == sign and board[2] == sign) or \
           (board[12] == sign and board[9] == sign and board[6] == sign) or \
           (board[9] == sign and board[6] == sign and board[3] == sign) or \
           (board[13] == sign and board[10] == sign and board[7] == sign):
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

# ab = ADS()
# ab.find_subsets()
# ab.display_metrics()
# # ab.run_test_case(TicTacToe())
