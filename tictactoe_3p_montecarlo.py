import random
from collections import defaultdict, deque
import numpy as np
from tictactoe_3p import TicTacToe3P, Sign, Status, ActionDomain, ResDom
from ADS_tictactoe_3p import ADS
from board_to_string_3p import board_to_string, string_to_board
import random

class MonteCarloTester:
    def __init__(self, num_runs, initial_sequences=10):
        self.num_runs = num_runs
        self.transition_counts = defaultdict(lambda: defaultdict(int))
        self.total_transitions = defaultdict(int)
        self.adjusted_maxlen = max(100, num_runs // 100)  # Dynamic adjustment based on number of runs
        self.recent_predictions = {
            'total': deque(maxlen=self.adjusted_maxlen),
            'draw': deque(maxlen=self.adjusted_maxlen),
            'cpu1_win': deque(maxlen=self.adjusted_maxlen),
            'cpu2_win': deque(maxlen=self.adjusted_maxlen),
            'user_win': deque(maxlen=self.adjusted_maxlen)
        }
        self.results_variance = {
            'total': deque(maxlen=self.adjusted_maxlen),
            'draw': deque(maxlen=self.adjusted_maxlen),
            'cpu1_win': deque(maxlen=self.adjusted_maxlen),
            'cpu2_win': deque(maxlen=self.adjusted_maxlen),
            'user_win': deque(maxlen=self.adjusted_maxlen)
        }

    def record_transition(self, before_state, after_state):
        self.transition_counts[before_state][after_state] += 1
        self.total_transitions[before_state] += 1

    def predict_state(self, current_state):
        if current_state not in self.transition_counts:
            return None
        transitions = self.transition_counts[current_state]
        total = self.total_transitions[current_state]
        probabilities = {state: count / total for state, count in transitions.items()}
        return max(probabilities, key=probabilities.get)

    def test_sequence(self, game):
        user_passed = 0
        user_failed = 0
        cpu1_passed = 0
        cpu1_failed = 0
        cpu2_passed = 0
        cpu2_failed = 0
        board_passed = 0
        board_failed = 0

        correct_predictions = {key: 0 for key in self.recent_predictions}
        total_predictions = {key: 0 for key in self.recent_predictions}

        while game.res == ResDom.PLAYING:
            before_state = self.serialize_game_state(game)
            predicted_next_state = self.predict_state(before_state)
            
            if game.status == Status.TURN_USER:
                game.uSelRow, game.uSelCol = random.choice([(r, c) for r in range(4) for c in range(4) if game.board[r][c] == Sign.EMPTY])
                game.action = ActionDomain.U_MOVE
            elif game.status == Status.TURN_COMP1:
                game.action = ActionDomain.C1_MOVE
            else:
                game.action = ActionDomain.C2_MOVE
            
            currentmoves = game.numOfMoves
            empty_cells = [(r, c) for r in range(4) for c in range(4) if game.board[r][c] == Sign.EMPTY]

            game.main()

            after_state = self.serialize_game_state(game)
            self.record_transition(before_state, after_state)

            result_type = 'total'
            if game.res == ResDom.TIE:
                result_type = 'draw'
            elif game.res == ResDom.C1_WON:
                result_type = 'cpu1_win'
            elif game.res == ResDom.C2_WON:
                result_type = 'cpu2_win'
            elif game.res == ResDom.U_WON:
                result_type = 'user_win'
            
            if predicted_next_state and predicted_next_state == after_state:
                self.recent_predictions[result_type].append(1)
                correct_predictions[result_type] += 1
            else:
                self.recent_predictions[result_type].append(0)
            
            total_predictions[result_type] += 1

            if game.action == ActionDomain.U_MOVE:
                try:
                    assert game.board[game.uSelRow][game.uSelCol] == Sign.CROSS
                    assert game.status == Status.TURN_COMP1
                    assert game.numOfMoves == currentmoves + 1
                    assert all(game.board[r][c] == Sign.EMPTY if (r, c) != (game.uSelRow, game.uSelCol) else game.board[r][c] == Sign.CROSS for r, c in empty_cells)
                    if game.res == ResDom.PLAYING:
                        assert True != game.winOnRow(game.uSelRow, game.uSelCol, Sign.CROSS) or True != game.winOnCol(game.uSelRow, game.uSelCol, Sign.CROSS) or True != game.winOnDiag(game.uSelRow, game.uSelCol, Sign.CROSS)
                    user_passed += 1
                except AssertionError:
                    print("User made an invalid move. Current board state:")
                    print('\n'.join(' '.join(cell.value for cell in row) for row in game.board))
                    print(f"User selected row {game.uSelRow} and column {game.uSelCol}")
                    user_failed += 1

            if game.action == ActionDomain.C1_MOVE:
                try:
                    assert game.status == Status.TURN_COMP2
                    assert game.numOfMoves == currentmoves + 1
                    assert sum(1 for r, c in empty_cells if game.board[r][c] == Sign.NOUGHT) == 1
                    cpu1_passed += 1
                except AssertionError:
                    print("CPU1 made an invalid move. Current board state:")
                    print('\n'.join(' '.join(cell.value for cell in row) for row in game.board))
                    cpu1_failed += 1

            if game.action == ActionDomain.C2_MOVE:
                try:
                    assert game.status == Status.TURN_USER
                    assert game.numOfMoves == currentmoves + 1
                    assert sum(1 for r, c in empty_cells if game.board[r][c] == Sign.BAR) == 1
                    cpu2_passed += 1
                except AssertionError:
                    print("CPU2 made an invalid move. Current board state:")
                    print('\n'.join(' '.join(cell.value for cell in row) for row in game.board))
                    cpu2_failed += 1

            try:
                assert all(cell in {Sign.CROSS, Sign.NOUGHT, Sign.BAR, Sign.EMPTY} for row in game.board for cell in row)
                assert abs(sum(row.count(Sign.CROSS) - row.count(Sign.NOUGHT) for row in game.board)) <= 1
                assert abs(sum(row.count(Sign.CROSS) - row.count(Sign.BAR) for row in game.board)) <= 1
                assert abs(sum(row.count(Sign.NOUGHT) - row.count(Sign.BAR) for row in game.board)) <= 1
                board_passed += 1
            except AssertionError:
                print("Invalid board state:")
                print('\n'.join(' '.join(cell.value for cell in row) for row in game.board))
                board_failed += 1
        
        self.update_variance()
        return (
            user_passed, user_failed, cpu1_passed, cpu1_failed, cpu2_passed, cpu2_failed, board_passed, board_failed, 
            correct_predictions, total_predictions
        )

    def serialize_game_state(self, game):
        return (tuple(tuple(cell.value for cell in row) for row in game.board), game.status.value, game.res.value)
    
    def update_variance(self):
        for key in self.results_variance:
            if len(self.recent_predictions[key]) > 10:  # Ensure enough data for variance calculation
                var = np.var([float(pred) for pred in self.recent_predictions[key]])
                self.results_variance[key].append(var)

    def calculate_reliability(self, predictions):
        if not predictions:
            return 0.0
        return (sum(predictions) / len(predictions)) * 100
    
    def calculate_stability(self):
        stability_scores = {}
        for key, variances in self.results_variance.items():
            if variances:
                mean_variance = np.mean(variances)
                stability_scores[key] = 100 - (mean_variance * 100)  # Convert variance to a reliability score
        return stability_scores
    
    def simulate_ADS(self, seq):
        ADS_true = 0
        ADS_false = 0
        ADS_tests = 0

        # initial step test
        game = TicTacToe3P()
        before_state_string = board_to_string(game.board)
        game.uSelRow, game.uSelCol = random.choice([(r, c) for r in range(4) for c in range(4) if game.board[r][c] == Sign.EMPTY])
        game.action = ActionDomain.U_MOVE

        game.main()

        try:
            transitions = seq.TrA_trails[before_state_string]['transitions']
            # transitions is a list of 4-tuples: (tile (0-9), user_turn boolean, game result, next state)
            # assert that the next state is in the list of possible transitions
            assert board_to_string(game.board) in [transition[3] for transition in transitions]
            # assign that element of the list to the variable 'transition'
            transition = next(transition for transition in transitions if transition[3] == board_to_string(game.board))
            if transition[1] == 0:
                assert game.status == Status.TURN_COMP1
                assert (4 * game.uSelRow + game.uSelCol) == transition[0]
            elif transition[1] == 1:
                assert game.status == Status.TURN_COMP2
            else:
                assert game.status == Status.TURN_USER
            assert game.res == transition[2]
            ADS_true += 1
        except AssertionError:
            print(f"ADS test failed for state: {before_state_string} and transitions: {transitions}")
            ADS_false += 1
        ADS_tests += 1

        # simulation step
        # find a random transition that has 7 empty tiles
        start_key = random.choice(seq.keylist)
        game.board = string_to_board(start_key)
        game.status = Status.TURN_USER
        game.numOfMoves = 9
        while game.res == ResDom.PLAYING:
            before_state_string = board_to_string(game.board)            
            if game.status == Status.TURN_USER:
                game.uSelRow, game.uSelCol = random.choice([(r, c) for r in range(4) for c in range(4) if game.board[r][c] == Sign.EMPTY])
                game.action = ActionDomain.U_MOVE
            elif game.status == Status.TURN_COMP1:
                game.action = ActionDomain.C1_MOVE
            else:
                game.action = ActionDomain.C2_MOVE
            game.main()

            try:
                transitions = seq.TrA[before_state_string]['transitions']
                # transitions is a list of 4-tuples: (tile (0-9), user_turn boolean, game result, next state)
                # assert that the next state is in the list of possible transitions
                assert board_to_string(game.board) in [transition[3] for transition in transitions]
                # assign that element of the list to the variable 'transition'
                transition = next(transition for transition in transitions if transition[3] == board_to_string(game.board))
                if transition[1] == 0:
                    assert game.status == Status.TURN_COMP1
                    assert (4 * game.uSelRow + game.uSelCol) == transition[0]
                elif transition[1] == 1:
                    assert game.status == Status.TURN_COMP2
                else:
                    assert game.status == Status.TURN_USER
                assert game.res == transition[2]
                ADS_true += 1
            except AssertionError:
                print(f"ADS test failed for state: {before_state_string} and transitions: {transitions}")
                ADS_false += 1
            ADS_tests += 1
        
        return ADS_true, ADS_false, ADS_tests

    def test_suite(self):
        sc_passed = 0
        sc_failed = 0
        others_passfail = [[0, 0], [0, 0], [0, 0], [0, 0]]  # [usermove, cpumove1, cpumove2, boardvalid]
        user_won = 0
        cpu1_won = 0
        cpu2_won = 0
        tie = 0

        results = {key: {'correct': 0, 'total': 0} for key in self.recent_predictions}

        seq = ADS()
        seq.find_subsets()

        ADS_true = 0
        ADS_false = 0
        ADS_tests = 0

        for i in range(self.num_runs):
            game = TicTacToe3P()
            (
                user_pass, user_fail, cpu1_pass, cpu1_fail, cpu2_pass, cpu2_fail, board_pass, board_fail, 
                correct, total
            ) = self.test_sequence(game)

            (
                ADS_t, ADS_f, ADS_total
            ) = self.simulate_ADS(seq)

            others_passfail[0][0] += user_pass
            others_passfail[0][1] += user_fail
            others_passfail[1][0] += cpu1_pass
            others_passfail[1][1] += cpu1_fail
            others_passfail[2][0] += cpu2_pass
            others_passfail[2][1] += cpu2_fail
            others_passfail[3][0] += board_pass
            others_passfail[3][1] += board_fail

            for key in results:
                results[key]['correct'] += correct[key]
                results[key]['total'] += total[key]

            ADS_true += ADS_t
            ADS_false += ADS_f
            ADS_tests += ADS_total
            try:
                # Check if the game ended in a valid state
                assert game.res in {ResDom.U_WON, ResDom.C1_WON, ResDom.C2_WON, ResDom.TIE}, "Invalid end state"
                # assert game win on row, column or diagonal, or tie
                assert game.res == ResDom.TIE or any(game.winOnRow(r, c, s) or game.winOnCol(r, c, s) or game.winOnDiag(r, c, s) for r in range(4) for c in range(4) for s in {Sign.CROSS, Sign.NOUGHT, Sign.BAR}), "Invalid end state"
                sc_passed += 1
                if game.res == ResDom.U_WON:
                    assert (game.winOnCol(r, c, Sign.CROSS) or game.winOnRow(r, c, Sign.CROSS) or game.winOnDiag(r, c, Sign.CROSS) for r in range(4) for c in range(4)), "User won but no winning row, column or diagonal"
                    user_won += 1
                elif game.res == ResDom.C1_WON:
                    assert (game.winOnCol(r, c, Sign.NOUGHT) or game.winOnRow(r, c, Sign.NOUGHT) or game.winOnDiag(r, c, Sign.NOUGHT) for r in range(4) for c in range(4)), "CPU1 won but no winning row, column or diagonal"
                    cpu1_won += 1
                elif game.res == ResDom.C2_WON:
                    assert (game.winOnCol(r, c, Sign.BAR) or game.winOnRow(r, c, Sign.BAR) or game.winOnDiag(r, c, Sign.BAR) for r in range(4) for c in range(4)), "CPU2 won but no winning row, column or diagonal"
                    cpu2_won += 1
                elif game.res == ResDom.TIE:
                    assert all(cell != Sign.EMPTY for row in game.board for cell in row), "Tie but empty cells still exist"
                    tie += 1
            except AssertionError as e:
                print(f"Test failed with error: {str(e)}")
                sc_failed += 1

        print(f"Tests passed: {sc_passed + others_passfail[0][0] + others_passfail[1][0] + others_passfail[2][0] + others_passfail[3][0]}")
        print(f"Tests failed: {sc_failed + others_passfail[0][1] + others_passfail[1][1] + others_passfail[2][1] + others_passfail[3][1]}")
        print("")
        print(f"End states invalid: {sc_failed}")
        print(f"User made invalid moves: {others_passfail[0][1]}")
        print(f"CPU1 made invalid moves: {others_passfail[1][1]}")
        print(f"CPU2 made invalid moves: {others_passfail[2][1]}")
        print(f"Invalid board states: {others_passfail[3][1]}")
        print("")
        print(f"User won: {user_won}")
        print(f"CPU1 won: {cpu1_won}")
        print(f"CPU2 won: {cpu2_won}")
        print(f"Tie: {tie}")
        print("")
        print(f"ADS tests passed: {ADS_true}")
        print(f"ADS tests failed: {ADS_false}")
        print(f"ADS tests total: {ADS_tests}")
        print("")
        print(f"Total runs: {i+1}")
        rel_values = []
        for key, value in results.items():
            if value['total'] > 0:
                reliability = self.calculate_reliability(self.recent_predictions[key])
                rel_values.append(reliability)
                print(f"Final {key.capitalize()} prediction reliability: {reliability:.2f}%")
        print("")
        while len(rel_values) < 5: # always returns 5 values
            rel_values.append(0.0)
        stab_values = []
        stability_scores = self.calculate_stability()
        for result_type, score in stability_scores.items():
            stab_values.append(score)
            print(f"Final {result_type.capitalize()} prediction stability score: {score:.2f}%")
        while len(stab_values) < 5:
            stab_values.append(1.0)
        return rel_values
        # return stab_values

# Run the test suite
tester = MonteCarloTester(10000)
tester.test_suite()
