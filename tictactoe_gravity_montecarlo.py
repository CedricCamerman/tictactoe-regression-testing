import random
from collections import defaultdict, deque
from time import time
import numpy as np
from tictactoe_gravity import TicTacToeGravity, Sign, Status, ActionDomain, ResDom
from ADS_tictactoe_gravity import ADS
from board_to_string_gravity import board_to_string


# Monte Carlo testing for Tic-Tac-Toe Gravity
class MonteCarloTester:
    def __init__(self, num_runs, initial_sequences=10):
        self.num_runs = num_runs
        self.transition_counts = defaultdict(lambda: defaultdict(int))
        self.total_transitions = defaultdict(int)
        self.adjusted_maxlen = max(100, num_runs // 100)  # Dynamic adjustment based on number of runs
        self.recent_predictions = {
            'total': deque(maxlen=self.adjusted_maxlen),
            'draw': deque(maxlen=self.adjusted_maxlen),
            'cpu_win': deque(maxlen=self.adjusted_maxlen),
            'user_win': deque(maxlen=self.adjusted_maxlen)
        }
        self.results_variance = {
            'total': deque(maxlen=self.adjusted_maxlen),
            'draw': deque(maxlen=self.adjusted_maxlen),
            'cpu_win': deque(maxlen=self.adjusted_maxlen),
            'user_win': deque(maxlen=self.adjusted_maxlen)
        }

    # Record a transition from one state to another
    def record_transition(self, before_state, after_state):
        self.transition_counts[before_state][after_state] += 1
        self.total_transitions[before_state] += 1

    # Predict the next state based on the current state
    def predict_state(self, current_state):
        if current_state not in self.transition_counts:
            return None
        transitions = self.transition_counts[current_state]
        total = self.total_transitions[current_state]
        probabilities = {state: count / total for state, count in transitions.items()}
        return max(probabilities, key=probabilities.get)

    # Test a sequence of moves in a game
    def test_sequence(self, game, seq):
        user_passed = 0
        user_failed = 0
        cpu_passed = 0
        cpu_failed = 0
        board_passed = 0
        board_failed = 0

        correct_predictions = {key: 0 for key in self.recent_predictions}
        total_predictions = {key: 0 for key in self.recent_predictions}

        ADS_true = 0
        ADS_false = 0
        ADS_tests = 0

        # Run the game until it ends
        while game.res == ResDom.PLAYING:
            # Record the state before the move
            before_state = self.serialize_game_state(game)
            before_state_string = board_to_string(game.board)
            predicted_next_state = self.predict_state(before_state)
            
            # Select a random move
            if game.status == Status.TURN_USER:
                game.uSelRow, game.uSelCol = random.choice([(r, c) for r in range(3) for c in range(3) if game.board[r][c] == Sign.EMPTY])
                game.action = ActionDomain.U_MOVE
            else:
                game.action = ActionDomain.C_MOVE
            
            currentmoves = game.numOfMoves
            empty_cells = [(r, c) for r in range(3) for c in range(3) if game.board[r][c] == Sign.EMPTY]

            # Make the move
            game.main()

            # Record the state after the move
            after_state = self.serialize_game_state(game)
            self.record_transition(before_state, after_state)

            # Record the result of the prediction
            result_type = 'total'
            if game.res == ResDom.TIE:
                result_type = 'draw'
            elif game.res == ResDom.C_WON:
                result_type = 'cpu_win'
            elif game.res == ResDom.U_WON:
                result_type = 'user_win'
            
            if predicted_next_state and predicted_next_state == after_state:
                self.recent_predictions[result_type].append(1)
                correct_predictions[result_type] += 1
            else:
                self.recent_predictions[result_type].append(0)
            
            total_predictions[result_type] += 1

            # Test the user move
            if game.action == ActionDomain.U_MOVE:
                try:
                    selected_row = min(r for r in range(3) if game.board[r][game.uSelCol] != Sign.EMPTY)
                    assert game.board[selected_row][game.uSelCol] == Sign.CROSS
                    assert game.status == Status.TURN_COMP
                    assert game.numOfMoves == currentmoves + 1
                    assert all(game.board[r][c] == Sign.EMPTY if (r, c) != (selected_row, game.uSelCol) else game.board[r][c] == Sign.CROSS for r, c in empty_cells)
                    if game.res == ResDom.PLAYING:
                        assert True != game.winOnRow(selected_row, game.uSelCol, Sign.CROSS) or True != game.winOnCol(selected_row, game.uSelCol, Sign.CROSS) or True != game.winOnDiag(selected_row, game.uSelCol, Sign.CROSS)
                    user_passed += 1
                except AssertionError:
                    user_failed += 1

            # Test the CPU move
            if game.action == ActionDomain.C_MOVE:
                try:
                    assert game.status == Status.TURN_USER
                    assert game.numOfMoves == currentmoves + 1
                    assert sum(1 for r, c in empty_cells if game.board[r][c] == Sign.NOUGHT) == 1
                    if game.res == ResDom.PLAYING:
                        assert True != any(game.winOnRow(r, c, Sign.NOUGHT) or game.winOnCol(r, c, Sign.NOUGHT) or game.winOnDiag(r, c, Sign.NOUGHT) for r, c in empty_cells if game.board[r][c] == Sign.NOUGHT)
                    cpu_passed += 1
                except AssertionError:
                    cpu_failed += 1

            # Test the board validity
            try:
                assert all(cell in {Sign.CROSS, Sign.NOUGHT, Sign.EMPTY} for row in game.board for cell in row)
                assert abs(sum(row.count(Sign.CROSS) - row.count(Sign.NOUGHT) for row in game.board)) <= 1
                assert all(game.board[r+1][c] != Sign.EMPTY for r in range(2) for c in range(3) if game.board[r][c] in {Sign.CROSS, Sign.NOUGHT})
                board_passed += 1
            except AssertionError:
                board_failed += 1

            # ADS test
            try:
                transitions = []
                if before_state_string in seq.TrA.keys():
                    transitions = seq.TrA[before_state_string]['transitions']
                    
                # assert that the next state is in the list of possible successors
                assert board_to_string(game.board) in [transition[3] for transition in transitions]

                # assert that input and output conform to the ADS
                transition = next(transition for transition in transitions if transition[3] == board_to_string(game.board))
                if transition[1]:
                    assert game.status == Status.TURN_COMP
                    # handling the issue of not knowing where the sign was dropped from
                    if game.uSelCol == 0:
                        assert transition[0] == 0 or transition[0] == 3 or transition[0] == 6
                    elif game.uSelCol == 1:
                        assert transition[0] == 1 or transition[0] == 4 or transition[0] == 7
                    else:
                        assert transition[0] == 2 or transition[0] == 5 or transition[0] == 8                
                else:
                    assert game.status == Status.TURN_USER
                assert game.res == transition[2]
                ADS_true += 1
            except AssertionError:
                ADS_false += 1
            ADS_tests += 1
        
        self.update_variance()
        return (
            user_passed, user_failed, cpu_passed, cpu_failed, board_passed, board_failed, 
            correct_predictions, total_predictions, ADS_true, ADS_false, ADS_tests
        )

    # Serialize the game state for prediction
    def serialize_game_state(self, game):
        return (tuple(tuple(cell.value for cell in row) for row in game.board), game.status.value, game.res.value)
    
    # Update the variance of the recent predictions
    def update_variance(self):
        for key in self.results_variance:
            if len(self.recent_predictions[key]) > 10:  # Ensure enough data for variance calculation
                var = np.var([float(pred) for pred in self.recent_predictions[key]])
                self.results_variance[key].append(var)

    # Calculate the reliability of the predictions
    def calculate_reliability(self, predictions):
        if not predictions:
            return 0.0
        return (sum(predictions) / len(predictions)) * 100
    
    # Calculate the stability of the predictions
    def calculate_stability(self):
        stability_scores = {}
        for key, variances in self.results_variance.items():
            if variances:
                mean_variance = np.mean(variances)
                stability_scores[key] = 100 - (mean_variance * 100)  # Convert variance to a reliability score
        return stability_scores

    # Run the test suite
    def test_suite(self):
        start_time = time()
        sc_passed = 0
        sc_failed = 0
        others_passfail = [[0, 0], [0, 0], [0, 0]]  # [usermove, cpumove, boardvalid]
        user_won = 0
        cpu_won = 0
        tie = 0

        results = {key: {'correct': 0, 'total': 0} for key in self.recent_predictions}

        seq = ADS()
        seq.find_subsets()

        ADS_true = 0
        ADS_false = 0
        ADS_tests = 0

        # Run the game N times
        for N in range(self.num_runs):
            game = TicTacToeGravity()
            (
                user_pass, user_fail, cpu_pass, cpu_fail, board_pass, board_fail, 
                correct, total, ADS_t, ADS_f, ADS_total
            ) = self.test_sequence(game, seq)

            others_passfail[0][0] += user_pass
            others_passfail[0][1] += user_fail
            others_passfail[1][0] += cpu_pass
            others_passfail[1][1] += cpu_fail
            others_passfail[2][0] += board_pass
            others_passfail[2][1] += board_fail

            ADS_true += ADS_t
            ADS_false += ADS_f
            ADS_tests += ADS_total

            for key in results:
                results[key]['correct'] += correct[key]
                results[key]['total'] += total[key]

            try:
                # Check if the game ended in a valid state
                assert game.res in {ResDom.U_WON, ResDom.C_WON, ResDom.TIE}, "Invalid end state"
                # assert game win on row, column or diagonal, or tie
                assert game.res == ResDom.TIE or any(game.winOnRow(r, c, s) or game.winOnCol(r, c, s) or game.winOnDiag(r, c, s) for r in range(3) for c in range(3) for s in {Sign.CROSS, Sign.NOUGHT}), "Invalid end state"
                sc_passed += 1
                if game.res == ResDom.U_WON:
                    assert (game.winOnCol(r, c, Sign.CROSS) or game.winOnRow(r, c, Sign.CROSS) or game.winOnDiag(r, c, Sign.CROSS) for r in range(3) for c in range(3)), "User won but no winning row, column or diagonal"
                    user_won += 1
                elif game.res == ResDom.C_WON:
                    assert (game.winOnCol(r, c, Sign.NOUGHT) or game.winOnRow(r, c, Sign.NOUGHT) or game.winOnDiag(r, c, Sign.NOUGHT) for r in range(3) for c in range(3)), "CPU won but no winning row, column or diagonal"
                    cpu_won += 1
                elif game.res == ResDom.TIE:
                    assert all(game.board[r][c] != Sign.EMPTY for r in range(3) for c in range(3)), "Tie but empty cells left"
                    tie += 1
            except AssertionError as e:
                # print(f"Test failed with error: {str(e)}")
                sc_failed += 1

        # Print the results
        print(f"Time taken: {time() - start_time:.2f} seconds")
        print(f"Tests passed: {sc_passed + others_passfail[0][0] + others_passfail[1][0] + others_passfail[2][0]}")
        print(f"Tests failed: {sc_failed + others_passfail[0][1] + others_passfail[1][1] + others_passfail[2][1]}")
        print("")
        print(f"End states invalid: {sc_failed}")
        print(f"User made invalid moves: {others_passfail[0][1]}")
        print(f"CPU made invalid moves: {others_passfail[1][1]}")
        print(f"Invalid board states: {others_passfail[2][1]}")
        print("")
        print(f"User won: {user_won}")
        print(f"CPU won: {cpu_won}")
        print(f"Tie: {tie}")
        print("")
        print(f"ADS tests passed: {ADS_true}")
        print(f"ADS tests failed: {ADS_false}")
        print(f"ADS tests total: {ADS_tests}")
        print("")
        print(f"Total runs: {N+1}")
        rel_values = []
        for key, value in results.items():
            if value['total'] > 0:
                reliability = self.calculate_reliability(self.recent_predictions[key])
                rel_values.append(reliability)
                print(f"Final {key.capitalize()} prediction reliability: {reliability:.2f}%")
        print("")
        while len(rel_values) < 4: # always returns 4 values
            rel_values.append(0.0)
        stab_values = []
        stability_scores = self.calculate_stability()
        for result_type, score in stability_scores.items():
            stab_values.append(score)
            print(f"Final {result_type.capitalize()} prediction stability score: {score:.2f}%")
        while len(stab_values) < 4:
            stab_values.append(1.0)
        # return rel_values
        return stab_values


# Run the test suite
tester = MonteCarloTester(1000)
tester.test_suite()
