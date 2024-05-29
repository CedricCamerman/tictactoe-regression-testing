import random
from collections import defaultdict, deque
import numpy as np
from tictactoe_ultimate import UltimateTicTacToe, Sign, Status, ActionDomain, ResDom

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
        cpu_passed = 0
        cpu_failed = 0
        board_passed = 0
        board_failed = 0

        correct_predictions = {key: 0 for key in self.recent_predictions}
        total_predictions = {key: 0 for key in self.recent_predictions}

        while game.res == ResDom.PLAYING:
            before_state = self.serialize_game_state(game)
            predicted_next_state = self.predict_state(before_state)
            
            if game.status == Status.TURN_USER:
                game.uSelBoardrow, game.uSelBoardcol = random.choice([(br, bc) for br in range(3) for bc in range(3) if game.board[br][bc].res == ResDom.PLAYING])
                game.uSelRow, game.uSelCol = random.choice([(r, c) for r in range(3) for c in range(3) if game.board[game.uSelBoardrow][game.uSelBoardcol].board[r][c] == Sign.EMPTY])
                game.action = ActionDomain.U_MOVE
            else:
                game.action = ActionDomain.C_MOVE
            
            currentmoves = game.numOfMoves
            empty_boards = [(br, bc) for br in range(3) for bc in range(3) if game.board[br][bc].res == ResDom.PLAYING]
            empty_cells = [(empty_boards.index((br, bc)), r, c) for br, bc in empty_boards for r in range(3) for c in range(3) if game.board[br][bc].board[r][c] == Sign.EMPTY]

            game.main()

            after_state = self.serialize_game_state(game)
            self.record_transition(before_state, after_state)

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

            if game.action == ActionDomain.U_MOVE:
                try:
                    assert game.board[game.uSelBoardrow][game.uSelBoardcol].board[game.uSelRow][game.uSelCol] == Sign.CROSS
                    assert game.status == Status.TURN_COMP
                    assert game.numOfMoves == currentmoves + 1
                    assert all(game.board[empty_boards[bn][0]][empty_boards[bn][1]].board[r][c] == Sign.EMPTY if (bn, r, c) != (empty_boards.index((game.uSelBoardrow, game.uSelBoardcol)), game.uSelRow, game.uSelCol) else game.board[empty_boards[bn][0]][empty_boards[bn][1]].board[r][c] == Sign.CROSS for bn, r, c in empty_cells)
                    if game.res == ResDom.PLAYING:
                        assert True != game.winOnRow(game.uSelBoardrow, game.uSelBoardcol, Sign.CROSS) or game.winOnCol(game.uSelBoardrow, game.uSelBoardcol, Sign.CROSS) or game.winOnDiag(game.uSelBoardrow, game.uSelBoardcol, Sign.CROSS)
                    user_passed += 1
                except AssertionError:
                    print("User made an invalid move. Current board state:")
                    print('\n'.join(' '.join(cell.value for cell in row) for row in game.board[game.uSelBoardrow][game.uSelBoardcol].board))
                    print(f"User selected boardrow {game.uSelBoardrow}, boardcol {game.uSelBoardcol}, row {game.uSelRow} and column {game.uSelCol}")
                    user_failed += 1

            if game.action == ActionDomain.C_MOVE:
                try:
                    assert game.status == Status.TURN_USER
                    assert game.numOfMoves == currentmoves + 1
                    assert sum(1 for bn, r, c in empty_cells if game.board[empty_boards[bn][0]][empty_boards[bn][1]].board[r][c] == Sign.NOUGHT) == 1
                    if game.res == ResDom.PLAYING:
                        assert True != game.winOnRow(empty_boards[empty_cells[0][0]][0], empty_boards[empty_cells[0][0]][1], Sign.NOUGHT) or game.winOnCol(empty_boards[empty_cells[0][0]][0], empty_boards[empty_cells[0][0]][1], Sign.NOUGHT) or game.winOnDiag(empty_boards[empty_cells[0][0]][0], empty_boards[empty_cells[0][0]][1], Sign.NOUGHT)
                    cpu_passed += 1
                except AssertionError:
                    print("CPU made an invalid move. Current board state:")
                    for i in range(3):
                        for _ in range(3):  # For each row in the inner 3x3 board
                            for j in range(3):  # For each 3x3 board in the row
                                print("|".join([game.board[i][j].board[_][col].value for col in range(3)]), end="   ")
                            print()
                        print("-" * 29)  # Print a separator line after each row of 3x3 boards
                    cpu_failed += 1

            try:
                assert all(cell in {Sign.CROSS, Sign.NOUGHT, Sign.EMPTY} for br in range(3) for bc in range(3) for row in game.board[br][bc].board for cell in row)
                assert abs(sum(row.count(Sign.CROSS) - row.count(Sign.NOUGHT) for br in range(3) for bc in range(3) for row in game.board[br][bc].board)) <= 1
                board_passed += 1
            except AssertionError:
                print("Invalid board state:")
                print('\n'.join(' '.join(cell.value for cell in row) for row in game.board[game.uSelBoardrow][game.uSelBoardcol].board))
                board_failed += 1
        
        self.update_variance()
        return (
            user_passed, user_failed, cpu_passed, cpu_failed, board_passed, board_failed, 
            correct_predictions, total_predictions
        )

    def serialize_game_state(self, game):
        return (tuple((tuple(tuple(cell.value for cell in row) for row in board.board), board.res.value) for board in [game.board[br][bc] for br in range(3) for bc in range(3)]), game.status.value, game.res.value)
    
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

    def test_suite(self):
        sc_passed = 0
        sc_failed = 0
        others_passfail = [[0, 0], [0, 0], [0, 0]]  # [usermove, cpumove, boardvalid]
        user_won = 0
        cpu_won = 0
        tie = 0

        results = {key: {'correct': 0, 'total': 0} for key in self.recent_predictions}

        for i in range(self.num_runs):
            game = UltimateTicTacToe()
            (
                user_pass, user_fail, cpu_pass, cpu_fail, board_pass, board_fail, 
                correct, total
            ) = self.test_sequence(game)

            others_passfail[0][0] += user_pass
            others_passfail[0][1] += user_fail
            others_passfail[1][0] += cpu_pass
            others_passfail[1][1] += cpu_fail
            others_passfail[2][0] += board_pass
            others_passfail[2][1] += board_fail

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
                    assert all(game.board[r][c].res != ResDom.PLAYING for r in range(3) for c in range(3)), "Tie but playing boards left"
                    tie += 1
            except AssertionError as e:
                print(f"Test failed with error: {str(e)}")
                sc_failed += 1

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
        print(f"Total runs: {i+1}")
        for key, value in results.items():
            if value['total'] > 0:
                reliability = self.calculate_reliability(self.recent_predictions[key])
                print(f"Final {key.capitalize()} prediction reliability: {reliability:.2f}%")
        print("")

        stability_scores = self.calculate_stability()
        for result_type, score in stability_scores.items():
            print(f"Final {result_type.capitalize()} prediction stability score: {score:.2f}%")

# Run the test suite
tester = MonteCarloTester(10000)
tester.test_suite()
