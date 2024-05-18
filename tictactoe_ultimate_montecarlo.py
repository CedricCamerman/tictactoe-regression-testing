import random

from tictactoe_ultimate import UltimateTicTacToe, Sign, Status, ActionDomain, ResDom

# Test sequence
def test_sequence(game):
    user_passed = 0
    user_failed = 0
    cpu_passed = 0
    cpu_failed = 0
    board_passed = 0
    board_failed = 0

    # Play until game ends
    while game.res == ResDom.PLAYING:
        if game.status == Status.TURN_USER:
            # User makes a move
            game.uSelBoardrow, game.uSelBoardcol = random.choice([(br, bc) for br in range(3) for bc in range(3) if game.board[br][bc].res == ResDom.PLAYING])
            game.uSelRow, game.uSelCol = random.choice([(r, c) for r in range(3) for c in range(3) if game.board[game.uSelBoardrow][game.uSelBoardcol].board[r][c] == Sign.EMPTY])
            game.action = ActionDomain.U_MOVE
        else:
            # CPU makes a move
            game.action = ActionDomain.C_MOVE
        
        currentmoves = game.numOfMoves
        empty_boards = [(br, bc) for br in range(3) for bc in range(3) if game.board[br][bc].res == ResDom.PLAYING]
        # get all empty cells in all boards in format (boardnumber, row, column) where boardnumber is the index of the board in empty_boards
        empty_cells = [(empty_boards.index((br, bc)), r, c) for br, bc in empty_boards for r in range(3) for c in range(3) if game.board[br][bc].board[r][c] == Sign.EMPTY]

        # Execute action protocol based on turn
        game.main()

        # Check if the user made a valid move
        if game.action == ActionDomain.U_MOVE:
            # try assertion to check if the user made a valid move
            try:
                assert game.board[game.uSelBoardrow][game.uSelBoardcol].board[game.uSelRow][game.uSelCol] == Sign.CROSS
                assert game.status == Status.TURN_COMP
                assert game.numOfMoves == currentmoves + 1
                # assert that all empty_cells from before are still empty except the selected cell
                assert all(game.board[empty_boards[bn][0]][empty_boards[bn][1]].board[r][c] == Sign.EMPTY if (bn, r, c) != (empty_boards.index((game.uSelBoardrow, game.uSelBoardcol)), game.uSelRow, game.uSelCol) else game.board[empty_boards[bn][0]][empty_boards[bn][1]].board[r][c] == Sign.CROSS for bn, r, c in empty_cells)
                user_passed += 1

            except AssertionError:
                # print error reason and current board state and chosen move
                print("User made an invalid move. Current board state:")
                print('\n'.join(' '.join(cell.value for cell in row) for row in game.board[game.uSelBoardrow][game.uSelBoardcol].board))
                print(f"User selected boardrow {game.uSelBoardrow}, boardcol {game.uSelBoardcol}, row {game.uSelRow} and column {game.uSelCol}")
                user_failed += 1

        # Check if the CPU made a valid move
        if game.action == ActionDomain.C_MOVE:
            # try assertion to check if the CPU made a valid move
            try:
                assert game.status == Status.TURN_USER
                assert game.numOfMoves == currentmoves + 1
                # assert that only one cell from empty_cells from before is filled with NOUGHT
                assert sum(1 for bn, r, c in empty_cells if game.board[empty_boards[bn][0]][empty_boards[bn][1]].board[r][c] == Sign.NOUGHT) == 1
                cpu_passed += 1

            except AssertionError:
                # print error reason and current board state
                print("CPU made an invalid move. Current board state:")
                for i in range(3):
                    for _ in range(3):  # For each row in the inner 3x3 board
                        for j in range(3):  # For each 3x3 board in the row
                            print("|".join([game.board[i][j].board[_][col].value for col in range(3)]), end="   ")
                        print()
                    print("-" * 29)  # Print a separator line after each row of 3x3 boards
                cpu_failed += 1

        # Check if the board state is valid
        try:
            assert all(cell in {Sign.CROSS, Sign.NOUGHT, Sign.EMPTY} for br in range(3) for bc in range(3) for row in game.board[br][bc].board for cell in row)
            assert abs(sum(row.count(Sign.CROSS) - row.count(Sign.NOUGHT) for br in range(3) for bc in range(3) for row in game.board[br][bc].board)) <= 1
            board_passed += 1
        except AssertionError:
            # print error reason and current board state
            print("Invalid board state:")
            print('\n'.join(' '.join(cell.value for cell in row) for row in game.board[game.uSelBoardrow][game.uSelBoardcol].board))
            board_failed += 1
        
    return user_passed, user_failed, cpu_passed, cpu_failed, board_passed, board_failed

# Test suite
def test_suite(num_runs):
    sc_passed = 0
    sc_failed = 0
    others_passfail = [[0, 0], [0, 0], [0, 0]] # [usermove, cpumove, boardvalid]
    user_won = 0
    cpu_won = 0
    tie = 0
    for _ in range(num_runs):
        # Initialize game
        game = UltimateTicTacToe()

        # Run the test sequence
        user_pass, user_fail, cpu_pass, cpu_fail, board_pass, board_fail = test_sequence(game)
        others_passfail[0][0] += user_pass
        others_passfail[0][1] += user_fail
        others_passfail[1][0] += cpu_pass
        others_passfail[1][1] += cpu_fail
        others_passfail[2][0] += board_pass
        others_passfail[2][1] += board_fail

        try:
            # Check if the game ended in a valid state
            assert game.res in {ResDom.U_WON, ResDom.C_WON, ResDom.TIE}, "Invalid end state"
            # assert game win on row, column or diagonal, or tie
            assert game.res == ResDom.TIE or any(game.winOnRow(r, c, s) or game.winOnCol(r, c, s) or game.winOnDiag(r, c, s) for r in range(3) for c in range(3) for s in {Sign.CROSS, Sign.NOUGHT}), "Invalid end state"
            sc_passed += 1
            if game.res == ResDom.U_WON:
                user_won += 1
            elif game.res == ResDom.C_WON:
                cpu_won += 1
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
    print(f"CPU made invalid moves: {others_passfail[1][1]}")
    print(f"Invalid board states: {others_passfail[2][1]}")
    print("")
    print(f"User won: {user_won}")
    print(f"CPU won: {cpu_won}")
    print(f"Tie: {tie}")

# Run the test suite
test_suite(200)
