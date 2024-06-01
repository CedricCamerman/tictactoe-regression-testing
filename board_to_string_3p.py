from tictactoe_3p import Sign, Status, ActionDomain, ResDom

def board_to_string(board):
    # Convert the board to a string representation on a single line. empty = '_', cross = 'X', nought = 'O'
    board_str = ''
    for row in board:
        for cell in row:
            if cell == Sign.EMPTY:
                board_str += '_'  # empty cell
            elif cell == Sign.CROSS:
                board_str += 'X'
            elif cell == Sign.NOUGHT:
                board_str += 'O'
            else:
                board_str += '/'
    return board_str

# string to board
def string_to_board(board_str):
    # Convert the string representation of the board to a 4x4 list
    board = [[Sign.EMPTY] * 4 for _ in range(4)]
    for i, cell in enumerate(board_str):
        row = i // 4
        col = i % 4
        if cell == '_':
            board[row][col] = Sign.EMPTY
        elif cell == 'X':
            board[row][col] = Sign.CROSS
        elif cell == 'O':
            board[row][col] = Sign.NOUGHT
        else:
            board[row][col] = Sign.BAR
    return board
