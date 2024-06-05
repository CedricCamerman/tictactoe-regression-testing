import random
from tictactoe import TicTacToe, Sign, Status, ActionDomain, ResDom


# Tic-Tac-Toe game class
class UltimateTicTacToe:
    def __init__(self):
        self.board = [[TicTacToe() for _ in range(3)] for _ in range(3)]
        self.status = Status.TURN_USER  # User starts
        self.uSelCol = None
        self.uSelRow = None
        self.uSelBoardrow = None
        self.uSelBoardcol = None
        self.action = ActionDomain.U_MOVE
        self.res = ResDom.PLAYING
        self.numOfMoves = 0

    # Winning conditions
    def winOnRow(self, r, c, s):
        if s == Sign.CROSS:
            return all(self.board[r][col].res == ResDom.U_WON for col in range(3))
        else:
            return all(self.board[r][col].res == ResDom.C_WON for col in range(3))

    def winOnCol(self, r, c, s):
        if s == Sign.CROSS:
            return all(self.board[row][c].res == ResDom.U_WON for row in range(3))
        else:
            return all(self.board[row][c].res == ResDom.C_WON for row in range(3))

    def winOnDiag(self, r, c, s):
        if s == Sign.CROSS:
            if all(self.board[i][i].res == ResDom.U_WON for i in range(3)):
                return True
            if all(self.board[i][2 - i].res == ResDom.U_WON for i in range(3)):
                return True
            else:
                return False
        else:
            if all(self.board[i][i].res == ResDom.C_WON for i in range(3)):
                return True
            if all(self.board[i][2 - i].res == ResDom.C_WON for i in range(3)):
                return True
            else:
                return False

    # Make a move
    def makeMove(self, br, bc, r, c, s):
        self.numOfMoves += 1
        self.board[br][bc].makeMove(r, c, s)
        # Check whether game state has to change
        if self.winOnRow(br, bc, s) or self.winOnCol(br, bc, s) or self.winOnDiag(br, bc, s):
            if s == Sign.CROSS:
                self.res = ResDom.U_WON
            elif s == Sign.NOUGHT:
                self.res = ResDom.C_WON
        elif self.numOfMoves == 81 or all(self.board[br][bc].res != ResDom.PLAYING for br in range(3) for bc in range(3)):
            self.res = ResDom.TIE

    # When user makes a move
    def moveUser(self):
        if self.status == Status.TURN_USER:
            if self.board[self.uSelBoardrow][self.uSelBoardcol].res == ResDom.PLAYING and self.board[self.uSelBoardrow][self.uSelBoardcol].board[self.uSelRow][self.uSelCol] == Sign.EMPTY:
                self.makeMove(self.uSelBoardrow, self.uSelBoardcol, self.uSelRow, self.uSelCol, Sign.CROSS)
                self.status = Status.TURN_COMP
            else:
                print("Invalid move! The selected position is already occupied or board is already finished.")

    # When computer makes a move
    def moveComp(self):
        if self.status == Status.TURN_COMP:
            # Find whether there are empty cells
            unf_boards = [(br, bc) for br in range(3) for bc in range(3) if self.board[br][bc].res == ResDom.PLAYING]
            if unf_boards:
                # Select a random empty board
                br, bc = random.choice(unf_boards)
                empty_cells = [(r, c) for r in range(3) for c in range(3) if self.board[br][bc].board[r][c] == Sign.EMPTY]
                if empty_cells:
                    # Select a random empty cell in the chosen board
                    r, c = random.choice(empty_cells)
                    self.makeMove(br, bc, r, c, Sign.NOUGHT)  # Update the state of the chosen board
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
#         for i in range(3):
#             for _ in range(3):  # For each row in the inner 3x3 board
#                 for j in range(3):  # For each 3x3 board in the row
#                     print("|".join([self.board[i][j].board[_][col].value for col in range(3)]), end="   ")
#                 print()
#             print("-" * 29)  # Print a separator line after each row of 3x3 boards

#     # Play loop; runs until game state is not PLAYING
#     def play(self):
#         print("Welcome to Ultimate Tic-Tac-Toe!")
#         while self.res == ResDom.PLAYING:
#             self.displayBoard()
#             if self.status == Status.TURN_USER:
#                 print("Your turn")
#                 while True:
#                     try:
#                         self.uSelBoardrow = int(input("Enter boardrow (0, 1, 2): "))
#                         self.uSelBoardcol = int(input("Enter boardcol (0, 1, 2): "))
#                         self.uSelRow = int(input("Enter row (0, 1, 2): "))
#                         self.uSelCol = int(input("Enter column (0, 1, 2): "))
#                         if 0 <= self.uSelRow <= 2 and 0 <= self.uSelCol <= 2 and 0 <= self.uSelBoardrow <= 2 and 0 <= self.uSelBoardcol <= 2:
#                             break
#                         else:
#                             print("Invalid input! Row and column must be between 0 and 2.")
#                     except ValueError:
#                         print("Invalid input! Please enter integers for row and column.")
#                 self.action = ActionDomain.U_MOVE
#             else:
#                 print("Computer's turn")
#                 self.action = ActionDomain.C_MOVE
#             self.main()
#         if self.res == ResDom.U_WON:
#             print("Congratulations! You won!")
#         elif self.res == ResDom.C_WON:
#             print("Computer wins!")
#         else:
#             print("It's a tie!")

# # Initialize game
# game = UltimateTicTacToe()

# # Run game
# game.play()
