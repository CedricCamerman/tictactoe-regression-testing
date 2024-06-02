from tictactoe_gravity_states import Sign, Status, ActionDomain, ResDom
import random


class TicTacToeGravity:
    def __init__(self):
        self.board = [[Sign.EMPTY] * 3 for _ in range(3)]
        self.status = Status.TURN_USER  # User starts
        self.uSelCol = None
        self.uSelRow = None
        self.action = ActionDomain.U_MOVE
        self.res = ResDom.PLAYING
        self.numOfMoves = 0

    def winOnRow(self, r, c, s):
        return all(self.board[r][col] == s for col in range(3))

    def winOnCol(self, r, c, s):
        return all(self.board[row][c] == s for row in range(3))

    def winOnDiag(self, r, c, s):
        if r == c:
            if all(self.board[i][i] == s for i in range(3)):
                return True
        if r + c == 2:
            if all(self.board[i][2 - i] == s for i in range(3)):
                return True
        return False

    def makeMove(self, r, c, s):
        if self.board[0][c] != Sign.EMPTY:
            print("Column is full. Please choose another column.")
            return False

        # Find the lowest empty cell in the selected column
        for row in range(2, -1, -1):
            if self.board[row][c] == Sign.EMPTY:
                self.board[row][c] = s
                self.numOfMoves += 1

                # Check whether game state has to change
                if self.winOnRow(row, c, s) or self.winOnCol(row, c, s) or self.winOnDiag(row, c, s):
                    if s == Sign.CROSS:
                        self.res = ResDom.U_WON
                    elif s == Sign.NOUGHT:
                        self.res = ResDom.C_WON
                elif self.numOfMoves == 9:
                    self.res = ResDom.TIE
                return True

    def moveUser(self):
        if self.status == Status.TURN_USER:
            if self.board[self.uSelRow][self.uSelCol] == Sign.EMPTY:
                self.makeMove(self.uSelRow, self.uSelCol, Sign.CROSS)
                self.status = Status.TURN_COMP
            else:
                print("Invalid move! The selected position is already occupied.")

    def moveComp(self):
        if self.status == Status.TURN_COMP:
            empty_cells = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == Sign.EMPTY]
            if empty_cells:
                r, c = random.choice(empty_cells)
                self.makeMove(r, c, Sign.NOUGHT)
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
#                         self.uSelRow = int(input("Enter row (0, 1, 2): "))
#                         self.uSelCol = int(input("Enter column (0, 1, 2): "))
#                         if 0 <= self.uSelRow <= 2 and 0 <= self.uSelCol <= 2:
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
#         self.displayBoard()
#         if self.res == ResDom.U_WON:
#             print("Congratulations! You won!")
#         elif self.res == ResDom.C_WON:
#             print("Computer wins!")
#         else:
#             print("It's a tie!")


# # Initialize game
# game = TicTacToeGravity()

# # Run game
# game.play()
