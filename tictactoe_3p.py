from tictactoe_3p_states import Sign, Status, ActionDomain, ResDom
import random


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

    # Check whether a player has won on a diagonal, only three in a row needed. There are six diagonals to win on in a 4x4 board.
    def winOnDiag(self, r, c, s):
        # Top-left to bottom-right
        if (self.board[0][1] == s and self.board[1][2] == s and self.board[2][3] == s) or \
           (self.board[0][0] == s and self.board[1][1] == s and self.board[2][2] == s) or \
           (self.board[1][1] == s and self.board[2][2] == s and self.board[3][3] == s) or \
           (self.board[1][0] == s and self.board[2][1] == s and self.board[3][2] == s):
            return True
        
        # Bottom-left to top-right
        if (self.board[2][0] == s and self.board[1][1] == s and self.board[0][2] == s) or \
           (self.board[3][0] == s and self.board[2][1] == s and self.board[1][2] == s) or \
           (self.board[2][1] == s and self.board[1][2] == s and self.board[0][3] == s) or \
           (self.board[3][1] == s and self.board[2][2] == s and self.board[1][3] == s):
            return True

        return False

    # Make a move
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

    # When user makes a move
    def moveUser(self):
        if self.status == Status.TURN_USER:
            if self.board[self.uSelRow][self.uSelCol] == Sign.EMPTY:
                self.makeMove(self.uSelRow, self.uSelCol, Sign.CROSS)
                self.status = Status.TURN_COMP1
            else:
                print("Invalid move! The selected position is already occupied.")

    # When computer makes a move
    def moveComp(self):
        if self.status == Status.TURN_COMP1:
            empty_cells = [(r, c) for r in range(4) for c in range(4) if self.board[r][c] == Sign.EMPTY]
            if empty_cells:
                r, c = random.choice(empty_cells)
                self.makeMove(r, c, Sign.NOUGHT)
                self.status = Status.TURN_COMP2

        elif self.status == Status.TURN_COMP2:
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
                
#     # Display the board
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
