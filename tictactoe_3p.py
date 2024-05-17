from enum import Enum
import random

# Board tile states
class Sign(Enum):
    CROSS = 'X'
    NOUGHT = 'O'
    BAR = '/'
    EMPTY = ' '

# Game states
class Status(Enum):
    TURN_USER = 1
    TURN_COMP1 = 2
    TURN_COMP2 = 3

# Actions
class ActionDomain(Enum):
    U_MOVE = 1
    C1_MOVE = 2
    C2_MOVE = 3

# Result states
class ResDom(Enum):
    PLAYING = 1
    U_WON = 2
    C1_WON = 3
    C2_WON = 4
    TIE = 4

# Tic-Tac-Toe game class
class TicTacToe3P:
    # Initialize game with three players and 4x4 board
    def __init__(self):
        self.board = [[Sign.EMPTY] * 4 for _ in range(4)]
        self.status = Status.TURN_USER # User starts
        self.uSelCol = None
        self.uSelRow = None
        self.action = ActionDomain.U_MOVE
        self.res = ResDom.PLAYING
        self.numOfMoves = 0   

    # Check whether a player has won on a row, only three in a row needed
    def winOnRow(self, r, c, s):
        for i in range(2):
            if all(self.board[r][j] == s for j in range(i, i + 3)):
                return True
        return False

    # Check whether a player has won on a column, only three in a row needed
    def winOnCol(self, r, c, s):
        for i in range(2):
            if all(self.board[j][c] == s for j in range(i, i + 3)):
                return True
        return False

    # Check whether a player has won on a diagonal, only three in a row needed
    def winOnDiag(self, r, c, s):
        if r == c or r + c == 3:
            for i in range(2):
                if all(self.board[j][j] == s for j in range(i, i + 3)):
                    return True
                if all(self.board[j][3 - j] == s for j in range(i, i + 3)):
                    return True
        return False

    def makeMove(self, r, c, s):
        self.board[r][c] = s
        self.numOfMoves += 1

        # Check whether game state has to change
        if self.winOnRow(r, c, s) or self.winOnCol(r, c, s) or self.winOnDiag(r, c, s):
            if s == Sign.CROSS:
                self.res = ResDom.U_WON
            elif s == Sign.NOUGHT:
                self.res = ResDom.C1_WON
            elif s == Sign.BAR:
                self.res = ResDom.C2_WON
        elif self.numOfMoves == 16:
            self.res = ResDom.TIE

    def moveUser(self):
        if self.status == Status.TURN_USER:
            if self.board[self.uSelRow][self.uSelCol] == Sign.EMPTY:
                self.makeMove(self.uSelRow, self.uSelCol, Sign.CROSS)
                self.status = Status.TURN_COMP1
            else:
                print("Invalid move! The selected position is already occupied.")

    def moveComp(self):
        if self.status == Status.TURN_COMP1:
            empty_cells = [(r, c) for r in range(4) for c in range(4) if self.board[r][c] == Sign.EMPTY]
            if empty_cells:
                r, c = random.choice(empty_cells)
                self.makeMove(r, c, Sign.NOUGHT)
                self.status = Status.TURN_COMP2

        if self.status == Status.TURN_COMP2:
            empty_cells = [(r, c) for r in range(4) for c in range(4) if self.board[r][c] == Sign.EMPTY]
            if empty_cells:
                r, c = random.choice(empty_cells)
                self.makeMove(r, c, Sign.BAR)
                self.status = Status.TURN_USER

    # Execute action protocol based on turn    
    def main(self):
        if self.res == ResDom.PLAYING:
            if self.action == ActionDomain.U_MOVE:
                self.moveUser()
            else:
                self.moveComp()
    
#     def displayBoard(self):
#         for row in self.board:
#             print("|".join([sign.value for sign in row]))
#             print("-" * 5)

#     # Play loop; runs until game state is not PLAYING
#     def play(self):
#         print("Welcome to Tic-Tac-Toe!")
#         while self.res == ResDom.PLAYING:
#             self.displayBoard()
#             if self.status == Status.TURN_USER:
#                 print("Your turn")
#                 while True:
#                     try:
#                         self.uSelRow = int(input("Enter row (0, 1, 2, 3): "))
#                         self.uSelCol = int(input("Enter column (0, 1, 2, 3): "))
#                         if 0 <= self.uSelRow <= 3 and 0 <= self.uSelCol <= 3:
#                             break
#                         else:
#                             print("Invalid input! Row and column must be between 0 and 3.")
#                     except ValueError:
#                         print("Invalid input! Please enter integers for row and column.")
#                 self.action = ActionDomain.U_MOVE
#             else:
#                 print("Computer's turn")
#                 self.action = ActionDomain.C1_MOVE
#             self.main()
#         self.displayBoard()
#         if self.res == ResDom.U_WON:
#             print("Congratulations! You won!")
#         elif self.res == ResDom.C1_WON or self.res == ResDom.C2_WON:
#             print("Computer wins!")
#         else:
#             print("It's a tie!")


# # Initialize game
# game = TicTacToe3P()

# # Run game
# game.play()