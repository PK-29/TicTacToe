"""
    :platform: Windows
    :synopsis: This module allows you to Play a game of Tictactoe against the computer
    :Author: Prince

    Run this script using Python 3 on commandterminal then follow intructions on the terminal
    7|8|9  --> select where you want to place your move based on the keyboard numpad
    4|5|6
    1|2|3
    laptop dont have numpad so 1|2|3
                               4|5|6
                               7|8|9
"""


class TicTacToe:
    '''This class sets up the game and computes the computer game and draws out the board
    according to your move
    Attributes:
        self.gameboard (list): the blank game board
        self.turn (list): holds the X or O
        self.player (str): keeps track of weather player is X or O
        self.computer (str): keeps track of weather computer is X or O
        self.turnNum(int): the curent move number
        self.lastindex(dic): holds the win and loss move for the computer if a win isnt possible
    Args:
        playerMark(int): decides whether player will be X or O
    '''

    def __init__(self, playerMark):
        self.gameboard = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
        self.turn = ['X', 'O']
        self.player = self.turn[playerMark]
        self.computer = self.turn[(playerMark+1) % 2]
        self.turnNum = 0
        self.lastindex = {}

    def printBoard(self):
        ''' Prints the board accordingly to the keyboard numpad using a 1d array
        '''
        gb = self.gameboard
        print(gb[0]+'|'+gb[1] + '|' + gb[2]
              + '\n------\n'
              + gb[3]+'|'+gb[4] + '|' + gb[5]
              + '\n------\n'
              + gb[6]+'|'+gb[7] + '|' + gb[8]
              + '\n\n')

    def getTurn(self, movenum):
        '''Get the turn as X or O given the turn number
        Args:
            movenum: The turn number
        '''
        return self.turn[movenum % 2]

    def gameComplete(self):
        '''travers through the columns, rows and diagnally of the game board to
            find the winner
        '''
        winner = ''
        for i in range(3):
            if self.gameboard[3*i] == self.gameboard[(3*i)+1] == self.gameboard[(3*i)+2]:
                winner = self.gameboard[3*i]
                break
            elif self.gameboard[i] == self.gameboard[i+3] == self.gameboard[i+6]:
                winner = self.gameboard[i]
                break
        if self.gameboard[0] == self.gameboard[4] == self.gameboard[8] or self.gameboard[2] == self.gameboard[4] == self.gameboard[6]:
            winner = self.gameboard[4]
        if winner == self.player:
            print("you won")

        elif winner == self.computer:
            print("you lose")
        else:
            print('Tie')

    def updateEarliest(self, earliest, turnNum, position, earliestKey):
        '''Update the win and loss moves for the computer in the given dictionary
        Args:
            earliest: the dictionary holding the earliest move to win and earliest move that lead to
                    {'win': (10, 10), 'loss': (10, 10)}
            loss info for the computer
            turnNum: The turnnumber that decides how early computer can win
            position: the index to make the move in
            earliestKey: if the move is a win or a loss

        '''
        if turnNum < earliest[earliestKey][0]:
            earliest[earliestKey] = (turnNum, position)

    def checkResult(self, gameboard=None):
        '''check if the game is over for given gameboard or if none given then the class gamebord

        '''
        gb = gameboard
        if gb == None:
            gb = self.gameboard

        if '-' not in gb:
            return 0

        elif gb[0] == gb[1] == gb[2] and gb[0] != '-' or gb[3] == gb[4] == gb[5] and gb[3] != '-' or gb[6] == gb[7] == gb[8] and gb[6] != '-':
            return 1

        elif gb[2] == gb[5] == gb[8] and gb[2] != '-' or gb[1] == gb[4] == gb[7] and gb[1] != '-' or gb[0] == gb[3] == gb[6] and gb[0] != '-':
            return 1

        elif gb[2] == gb[4] == gb[6] and gb[2] != '-' or gb[0] == gb[4] == gb[8] and gb[0] != '-':
            return 1

        return -1

    def getEarliest(self, gameboard, turnNum, turn):
        '''Recurse through all possible moves of the given gameboard and store the earliest move
            that will lead to a win and the earliest move that will lead to a lose
         Args:
            gameboard: the given state of the gameboard
            turnNum: The turnnumber that decides how early computer can win
            turn: if its X or O

        '''
        earliest = {'win': (10, 10), 'loss': (10, 10)}

        currOutcome = 'loss' if turn == self.player else 'win'
        notTurn = 'X' if turn == 'O' else 'O'
        if '-' not in gameboard:
            self.updateEarliest(earliest, turnNum-1,
                                self.lastindex[turn], 'win')
            self.updateEarliest(earliest, turnNum,
                                self.lastindex[turn], 'loss')
            return earliest
        for i in range(9):
            if gameboard[i] != '-':
                continue
            gameboard[i] = turn
            self.lastindex[turn] = i
            if self.checkResult(gameboard) >= 0:
                self.updateEarliest(earliest, turnNum, i, currOutcome)
            else:
                predicted = self.getEarliest(gameboard, turnNum+1, notTurn)
                self.updateEarliest(
                    earliest, predicted['win'][0], predicted['win'][1], 'win')
                self.updateEarliest(
                    earliest, predicted['loss'][0], predicted['loss'][1], 'loss')
            gameboard[i] = '-'

        return earliest

    def makeCompMove(self):
        '''based on the result retrieved from get Earliest see if making the current move 
            will lead to a win if yes then make this move orif not check if the next move will lead to a lose
            and block the move

            Note:
                because of earliest move bot does not pick the middle since in the begining with little moves made
                the middle and the corner may be the same so picks whichever comes first
        '''
        # comment out to make bot less smart
        # ------------------
        # if self.gameboard[4] == '-':
        #     self.makeMove(4)
        # else:
        #     # -------------------
        earliest = self.getEarliest(
            self.gameboard, self.turnNum, self.turn[self.turnNum % 2])
        print(earliest)
        if earliest['win'][0] == self.turnNum and self.gameboard[earliest['win'][1]] == '-':
            print(self.gameboard[earliest['win'][1]])
            self.makeMove(earliest['win'][1])

        elif earliest['loss'][0] == self.turnNum + 1 and earliest['loss'][1] != 10:
            self.makeMove(earliest['loss'][1])

        else:
            self.makeMove(earliest['win'][1])

    def makeMove(self, move):
        '''given the index, mark the given move at the right plae in the board

        Args:
            move: the index to place the right mark
        '''
        if self.checkResult(self.gameboard) >= 0:
            self.gameComplete()
            return
        if 0 <= move <= 8 and '-' in self.gameboard:
            self.gameboard[move] = self.turn[self.turnNum % 2]
            self.turnNum += 1
        self.printBoard()

    def makePlayerMove(self):
        '''Take input from player and mark it in the board
        '''
        move = None
        if '-' not in self.gameboard or self.checkResult(self.gameboard) >= 0:
            return
        while move == None:
            temp = (int(input("Move: "))-1)
            if (0 <= temp <= 8) and self.gameboard[temp] == '-':
                move = temp
            else:
                print("move already played")

        self.makeMove(move)


if __name__ == '__main__':
    play = True
    alternate = -1
    while play:
        alternate += 1
        game1 = TicTacToe(alternate % 2)
        while game1.checkResult() < 0:
            if alternate % 2 == 0:
                game1.makePlayerMove()
                game1.makeCompMove()

            else:
                game1.makeCompMove()
                game1.makePlayerMove()

        if input("r to restart: ") != 'r':
            play = False
