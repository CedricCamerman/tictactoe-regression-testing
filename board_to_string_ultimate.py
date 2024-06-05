from tictactoe_ultimate import Sign, ResDom


# board to string lower boards
def board_to_stringa(board):
    # Convert the board to a string representation on a single line. empty = '_', cross = 'X', nought = 'O'
    board_str = ''
    for row in board:
        for cell in row:
            if cell == Sign.EMPTY:
                board_str += '_'  # empty cell
            elif cell == Sign.CROSS:
                board_str += 'X'
            else:
                board_str += 'O'
    return board_str

# board to string upper board
def board_to_stringb(result):
    # Convert the board to a string representation on a single line.
    board_str = ''
    if result == ResDom.PLAYING:
        board_str += '_'  # empty cell
    elif result == ResDom.U_WON:
        board_str += 'X'
    elif result == ResDom.C_WON:
        board_str += 'O'
    else: # draw
        board_str += '-'
    return board_str

# board to string upper board, row and column based
def board_to_stringc(board):
    # Convert the board to a string representation on a single line.
    board_str = ''
    for row in board:
        for cell in row:
            if cell.res == ResDom.PLAYING:
                board_str += '_'  # empty cell
            elif cell.res == ResDom.U_WON:
                board_str += 'X'
            elif cell.res == ResDom.C_WON:
                board_str += 'O'
            else: # draw
                board_str += '-'
    return board_str

# string to board
def string_to_board(board_str):
    # Convert the string representation of the board to a 3x3 list
    board = [[Sign.EMPTY] * 3 for _ in range(3)]
    for i, cell in enumerate(board_str):
        row = i // 3
        col = i % 3
        if cell == '_':
            board[row][col] = Sign.EMPTY
        elif cell == 'X':
            board[row][col] = Sign.CROSS
        else:
            board[row][col] = Sign.NOUGHT
    return board
