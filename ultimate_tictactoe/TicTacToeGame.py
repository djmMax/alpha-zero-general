from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .TicTacToeLogic import Board
import numpy as np
import math

"""
Game class implementation for the game of TicTacToe.
Based on the OthelloGame then getGameEnded() was adapted to new rules.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the OthelloGame by Surag Nair.
"""
class TicTacToeGame(Game):
    def __init__(self, n=3):
        self.n = n
        self.size = n**2

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(game2board(b))

    def getBoardSize(self):
        # (a,b) tuple
        return (self.size, self.size)

    def getActionSize(self):
        # return number of actions
        return self.size*self.size + 1

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        if action == self.size*self.size:
            return (board, -player)
        b = Board(self.n)
        b.pieces, b.active_cell = board2game(board, self.n)

        move = (int(action/self.size), action%self.size)
        b.execute_move(move, player)
        return (game2board(b), -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b.pieces, b.active_cell = board2game(board, self.n)

        legalMoves = b.get_legal_moves()
        if len(legalMoves)==0:
            valids[-1]=1
            return np.array(valids)
        for x, y in legalMoves:
            valids[self.size*x+y]=1
        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(self.n)
        b.pieces, b.active_cell = board2game(board, self.n)

        if b.is_win(player):
            return 1
        if b.is_win(-player):
            return -1
        if b.has_legal_moves():
            return 0
        # draw has a very little value
        return 1e-4

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        actives = np.where(board == 0.1)
        newboard = player*board
        newboard[actives] = 0.1
        return newboard

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.size**2+1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.size, self.size))
        l = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l

    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return board.tostring()

def board2game(board,n):
    pieces = np.copy(board)
    actives = np.where(pieces == np.float16(0.1))
    frees = np.where(pieces == 0)

    active_cell = (None, None)
    if frees[0].__len__() > 0 and actives[0].__len__() > 0:
        active_cell = (actives[0][0]//n, actives[1][0]//n)
        for i in range(actives[0].__len__()):
            if active_cell[0] != actives[0][i]//n or active_cell[1] != actives[1][i]//n:
                active_cell = (None, None)
                break

    pieces[frees] = 0
    pieces[actives] = 0

    return (pieces, active_cell)

def game2board(game):
    board = np.copy(game.pieces)

    for (x,y) in game.get_legal_moves():
        if(board[x][y]==0):
            board[x][y] = 0.1
    return board.astype(np.float16)

def display(board, action=None):
    size = board.shape[0]
    n =  math.floor(math.sqrt( size ))

    b = Board(n)
    b.pieces, b.active_cell = board2game(board, n)
    b.get_all_scores()

    print("   ", end="")
    for y in range(size):
        print (y,"", end="")
        if(y>0 and y%n==(n-1)):
            print("|",end="")
    print("")
    print("  ", end="")
    for _ in range(size):
        print ("-", end="-")
    print("----")
    for y in range(size):
        print(y, "|",end="")    # print the row #
        for x in range(size):
            score = b.scores[y//n][x//n]
            if score==1 :  print('\033[0;100m\033[95m', end='') # color win
            if score==0 :  print('\033[0;100m\033[94m', end='') # color null
            if score==-1:  print('\033[0;100m\033[92m', end='') # color win

            piece = board[y][x]    # get the piece to print
            if action == y*size + x : print('\033[91m', end='') #color action
            if piece == -1: print("X ",end="")
            elif piece == 1: print("O ",end="")
            elif piece == np.float16(0.1): print("\033[33m/ \033[0m",end="")
            else:
                print("- ",end="")
            if action == y*size + x : print("\033[0m", end='') #remove color action

            if score!=None :  print('\033[0m', end='') # end color

            if(x>0 and x%n==(n-1)):
                print("|",end="")
        print("")

        if(y>0 and y%n==(n-1)):
            print("  ", end="")
            for _ in range(size):
                print ("-", end="-")
            print("----")

    # for x in range(n):
    #     print(b.scores[x])

