from tictactoe_3p import TicTacToe3P, Sign, Status, ActionDomain, ResDom

import random

# Test sequence
def test_sequence(game):
    user_passed = 0
    user_failed = 0
    cpu1_passed = 0
    cpu1_failed = 0
    cpu2_passed = 0
    cpu2_failed = 0
    board_passed = 0
    board_failed = 0

    # Play until game ends
    while game.res == ResDom.PLAYING:
        if game.status == Status.TURN_USER:
            # User makes a move
            game.uSelRow, game.uSelCol = random.choice([(r, c) for r in range(4) for c in range(4) if game.board[r][c] == Sign.EMPTY])
            game.action = ActionDomain.U_MOVE
        elif game.status == Status.TURN_COMP1:
            # CPU1 makes a move
            game.action = ActionDomain.C1_MOVE
        else:
            # CPU2 makes a move
            game.action = ActionDomain.C2_MOVE
        
        currentmoves = game.numOfMoves
        empty_cells = [(r, c) for r in range(4) for c in range(4) if game.board[r][c] == Sign.EMPTY]

        # Execute action protocol based on turn
        game.main()

        # Check if the user made a valid move
        if game.action == ActionDomain.U_MOVE:
            # try assertion to check if the user made a valid move
            try:
                assert game.board[game.uSelRow][game.uSelCol] == Sign.CROSS
                assert game.status == Status.TURN_COMP1
                assert game.numOfMoves == currentmoves + 1
                # assert that all empty_cells from before are still empty except the selected cell
                assert all(game.board[r][c] == Sign.EMPTY if (r, c) != (game.uSelRow, game.uSelCol) else game.board[r][c] == Sign.CROSS for r, c in empty_cells)
                user_passed += 1

            except AssertionError:
                # print error reason and current board state and chosen move
                print("User made an invalid move. Current board state:")
                print('\n'.join(' '.join(cell.value for cell in row) for row in game.board))
                print(f"User selected row {game.uSelRow} and column {game.uSelCol}")
                user_failed += 1

        # Check if the CPU1 made a valid move
        if game.action == ActionDomain.C1_MOVE:
            # try assertion to check if the CPU1 made a valid move
            try:
                assert game.status == Status.TURN_COMP2
                assert game.numOfMoves == currentmoves + 1
                # assert that only one cell from empty_cells from before is filled with NOUGHT
                assert sum(1 for r, c in empty_cells if game.board[r][c] == Sign.NOUGHT) == 1
                cpu1_passed += 1

            except AssertionError:
                # print error reason and current board state
                print("CPU1 made an invalid move. Current board state:")
                print('\n'.join(' '.join(cell.value for cell in row) for row in game.board))
                cpu1_failed += 1

        # Check if the CPU2 made a valid move
        if game.action == ActionDomain.C2_MOVE:
            # try assertion to check if the CPU2 made a valid move
            try:
                assert game.status == Status.TURN_USER
                assert game.numOfMoves == currentmoves + 1
                # assert that only one cell from empty_cells from before is filled with BAR
                assert sum(1 for r, c in empty_cells if game.board[r][c] == Sign.BAR) == 1
                cpu2_passed += 1

            except AssertionError:
                # print error reason and current board state
                print("CPU2 made an invalid move. Current board state:")
                print('\n'.join(' '.join(cell.value for cell in row) for row in game.board))
                cpu2_failed += 1

        # Check if the board state is valid
        try:
            assert all(cell in {Sign.CROSS, Sign.NOUGHT, Sign.BAR, Sign.EMPTY} for row in game.board for cell in row)
            assert abs(sum(row.count(Sign.CROSS) - row.count(Sign.NOUGHT) for row in game.board)) <= 1
            assert abs(sum(row.count(Sign.CROSS) - row.count(Sign.BAR) for row in game.board)) <= 1
            assert abs(sum(row.count(Sign.NOUGHT) - row.count(Sign.BAR) for row in game.board)) <= 1
            board_passed += 1
        except AssertionError:
            # print error reason and current board state
            print("Invalid board state:")
            print('\n'.join(' '.join(cell.value for cell in row) for row in game.board))
            board_failed += 1
        
    return user_passed, user_failed, cpu1_passed, cpu1_failed, cpu2_passed, cpu2_failed, board_passed, board_failed

# Test suite
def test_suite(num_runs):
    sc_passed = 0
    sc_failed = 0
    others_passfail = [[0, 0], [0, 0], [0, 0], [0, 0]] # [usermove, cpumove1, cpumove2, boardvalid]
    user_won = 0
    cpu1_won = 0
    cpu2_won = 0
    tie = 0
    for _ in range(num_runs):
        # Initialize game
        game = TicTacToe3P()

        # Run the test sequence
        user_pass, user_fail, cpu1_pass, cpu1_fail, cpu2_pass, cpu2_fail, board_pass, board_fail = test_sequence(game)
        others_passfail[0][0] += user_pass
        others_passfail[0][1] += user_fail
        others_passfail[1][0] += cpu1_pass
        others_passfail[1][1] += cpu1_fail
        others_passfail[2][0] += cpu2_pass
        others_passfail[2][1] += cpu2_fail
        others_passfail[3][0] += board_pass
        others_passfail[3][1] += board_fail

        try:
            # Check if the game ended in a valid state
            assert game.res in {ResDom.U_WON, ResDom.C1_WON, ResDom.C2_WON, ResDom.TIE}, "Invalid end state"
            # assert game win on row, column or diagonal, or tie
            assert game.res == ResDom.TIE or any(game.winOnRow(r, c, s) or game.winOnCol(r, c, s) or game.winOnDiag(r, c, s) for r in range(4) for c in range(4) for s in {Sign.CROSS, Sign.NOUGHT, Sign.BAR}), "Invalid end state"
            sc_passed += 1
            if game.res == ResDom.U_WON:
                user_won += 1
            elif game.res == ResDom.C1_WON:
                cpu1_won += 1
            elif game.res == ResDom.C2_WON:
                cpu2_won += 1
            elif game.res == ResDom.TIE:
                tie += 1
        except AssertionError as e:
            print(f"Test failed with error: {str(e)}")
            sc_failed += 1

    # Print the summary
    print(f"Tests passed: {sc_passed + sum(passed for passed, _ in others_passfail)}")
    print(f"Tests failed: {sc_failed + sum(failed for _, failed in others_passfail)}")
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

# Run the test suite
test_suite(1000)
