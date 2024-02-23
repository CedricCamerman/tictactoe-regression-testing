from enum import Enum
import random

class Sign(Enum):
    CROSS = 'X'
    NOUGHT = 'O'
    EMPTY = ' '

class Status(Enum):
    TURN_USER = 1
    TURN_COMP = 2

class ActionDomain(Enum):
    U_MOVE = 1
    C_MOVE = 2

class ResDom(Enum):
    PLAYING = 1
    U_WON = 2
    C_WON = 3
    TIE = 4

class TicTacToe:
    def __init__(self):
        self.board = [[Sign.EMPTY] * 3 for _ in range(3)]
        self.status = Status.TURN_USER
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
        self.board[r][c] = s
        self.numOfMoves += 1
        if self.winOnRow(r, c, s) or self.winOnCol(r, c, s) or self.winOnDiag(r, c, s):
            if s == Sign.CROSS:
                self.res = ResDom.U_WON
            elif s == Sign.NOUGHT:
                self.res = ResDom.C_WON
        elif self.numOfMoves == 9:
            self.res = ResDom.TIE

    def moveUser(self):
        if self.status == Status.TURN_USER and self.board[self.uSelRow][self.uSelCol] == Sign.EMPTY:
            self.makeMove(self.uSelRow, self.uSelCol, Sign.CROSS)
            self.status = Status.TURN_COMP

    def moveComp(self):
        if self.status == Status.TURN_COMP:
            empty_cells = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == Sign.EMPTY]
            if empty_cells:
                r, c = random.choice(empty_cells)
                self.makeMove(r, c, Sign.NOUGHT)
                self.status = Status.TURN_USER

    def main(self):
        if self.res == ResDom.PLAYING:
            if self.action == ActionDomain.U_MOVE:
                self.moveUser()
            else:
                self.moveComp()
    
    def displayBoard(self):
        for row in self.board:
            print("|".join([sign.value for sign in row]))
            print("-" * 5)

    def play(self):
        print("Welcome to Tic-Tac-Toe!")
        while self.res == ResDom.PLAYING:
            self.displayBoard()
            if self.status == Status.TURN_USER:
                print("Your turn")
                self.uSelRow = int(input("Enter row (0, 1, 2): "))
                self.uSelCol = int(input("Enter column (0, 1, 2): "))
                self.action = ActionDomain.U_MOVE
            else:
                print("Computer's turn")
                self.action = ActionDomain.C_MOVE
            self.main()
        self.displayBoard()
        if self.res == ResDom.U_WON:
            print("Congratulations! You won!")
        elif self.res == ResDom.C_WON:
            print("Computer wins!")
        else:
            print("It's a tie!")

# Usage
game = TicTacToe()
game.play()
