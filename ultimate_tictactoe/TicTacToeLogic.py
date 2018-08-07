'''
Board class for the game of TicTacToe.
Default board size is 3x3.
Board data:
  1=white(O), -1=black(X), 0=empty
  first dim is column , 2nd is row:
     pieces[0][0] is the top left square,
     pieces[2][0] is the bottom left square,
Squares are stored and manipulated as (x,y) tuples.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the board for the game of Othello by Eric P. Nichols.

'''
# from bkcharts.attributes import color
class Board():

    # list of all 8 directions on the board, as (x,y) offsets
    __directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

    def __init__(self, n=3):
        "Set up initial board configuration."

        self.n = n
        self.size = n**2
        self.active_cell = (None,None)
        # Create the empty board array.
        self.pieces = [None]*self.size
        for i in range(self.size):
            self.pieces[i] = [0.]*self.size

        # Create the empty cell scores array.
        self.scores = [None]*self.n
        for i in range(self.n):
            self.scores[i] = [None]*self.n

    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]


    def get_cell_legal_moves(self,cell):
        """Returns all the legal moves for in the cell
        @param cell = (x,y) coordinate of the cell.        
        """

        moves = set()  # stores the legal moves.
        (x_, y_) = cell

        cell_score = self.get_cell_score(x_, y_)
        if(cell_score!=None):
            return list(moves)

        # Get all the empty squares (color==0)
        for y in range(y_*self.n, (y_+1)*self.n):
            for x in range(x_*self.n, (x_+1)*self.n):
                if self[x][y]==0:
                    newmove = (x, y)
                    moves.add(newmove)
        return list(moves)

    def has_cell_legal_moves(self,cell):
        (x_, y_) = cell

        cell_score = self.get_cell_score(x_, y_)
        if(cell_score!=None):
            return False

        # Get all the empty squares (color==0)
        for y in range(y_*self.n, (y_+1)*self.n):
            for x in range(x_*self.n, (x_+1)*self.n):
                if self[x][y]==0:
                    return True
        return False

    def get_legal_moves(self):
        """Returns all the legal moves   
        """
        moves = set()  # stores the legal moves.

        if(self.active_cell[0]==None):
            # Get all the empty squares (color==0)
            for y in range(self.n):
                for x in range(self.n):
                    if self.scores[x][y]==None:
                        newmove = self.get_cell_legal_moves((x,y))
                        moves.update(newmove)
        else:
            newmove = self.get_cell_legal_moves(self.active_cell)
            moves.update(newmove)

            #if we dont have moves in the current cell
            if(moves.__len__()==0):
                self.active_cell = (None,None)
                return self.get_legal_moves()

        return list(moves)

    def has_legal_moves(self):
        if(self.active_cell[0]==None):
            # Get all the empty squares (color==0)
            for y in range(self.n):
                for x in range(self.n):
                    if self.scores[x][y]==None:
                        return True
            return False
        else:
            if( self.has_cell_legal_moves(self.active_cell) ):
                return True
            else:
                self.active_cell = (None,None)
                return self.has_legal_moves()
    
    def get_cell_score(self, cell_x, cell_y):
        """Check whether the given player has collected a triplet in any direction; 
        @param color (1=white,-1=black)
        """
        win = self.n-1

        x_start = cell_x*self.n
        y_start = cell_y*self.n
        x_end   = (cell_x+1)*self.n
        y_end   = (cell_y+1)*self.n

        # check y-strips
        for y in range(y_start,y_end):
            count = 0
            for x in range(x_start,x_end-1):
                if self[x][y] and self[x][y]==self[x+1][y]:
                    count += 1
            if count==win:
                return self[x_start][y]
        # check x-strips
        for x in range(x_start,x_end):
            count = 0
            for y in range(y_start,y_end-1):
                if self[x][y] and self[x][y]==self[x][y+1]:
                    count += 1
            if count==win:
                return self[x][y_start]
        # check two diagonal strips
        count = 0
        for d in range(self.n-1):
            if self[x_start+d][y_start+d] and self[x_start+d][y_start+d]==self[x_start+d+1][y_start+d+1]:
                count += 1
        if count==win:
            return self[x_start][y_start]
        count = 0
        for d in range(self.n-1):
            if self[x_start+d][y_start+self.n-d-1] and self[x_start+d][y_start+self.n-d-1]==self[x_start+d+1][y_start+self.n-d-2]:
                count += 1
        if count==win:
            return self[x_start][y_start+self.n-1]
        
        #check null (all case filled)
        for y in range(self.n):
            for x in range(self.n):
                if self[x_start+x][y_start+y]==0:
                    return None
        # return 0 for null score
        return 0 
    
    def get_all_scores(self):
        for x_ in range(self.n):
            for y_ in range(self.n):
                self.scores[x_][y_] = self.get_cell_score(x_, y_)
        return self.scores

    def is_win(self, color):
        """Check whether the given player has collected a triplet in any direction; 
        @param color (1=white,-1=black)
        """
        win = self.n

        self.get_all_scores()

        # check y-strips
        for y in range(self.n):
            count = 0
            for x in range(self.n):
                if self.scores[x][y]==color:
                    count += 1
            if count==win:
                return True
        # check x-strips
        for x in range(self.n):
            count = 0
            for y in range(self.n):
                if self.scores[x][y]==color:
                    count += 1
            if count==win:
                return True
        # check two diagonal strips
        count = 0
        for d in range(self.n):
            if self.scores[d][d]==color:
                count += 1
        if count==win:
            return True
        count = 0
        for d in range(self.n):
            if self.scores[d][self.n-d-1]==color:
                count += 1
        if count==win:
            return True

        count_win, count_loss, count_null, is_full = 0,0,0, True
        #check if has majority
        for y in range(self.n):
            for x in range(self.n):
                if self.scores[x][y]==None:
                    is_full = False
                elif self.scores[x][y]==color:
                    count_win += 1
                elif self.scores[x][y]==-color:
                    count_loss += 1
                else:
                    count_null += 1

        if is_full:
            return count_win > count_loss
        else:
            return False
            #return count_win > (self.n**2 - count_win-count_null) #no place for the adversair to win

    def execute_move(self, move, color):
        """Perform the given move on the board; 
        color gives the color pf the piece to play (1=white,-1=black)
        """
    
        (x,y) = move
        
        # if(self.active_cell[0]!=None):
        #     x = x + self.active_cell[0]*self.n
        #     y = y + self.active_cell[1]*self.n

        # Add the piece to the empty square.
        assert self[x][y] == 0
        self[x][y] = color

        cell_x, cell_y = x//self.n, y//self.n
        self.scores[cell_x][cell_y] = self.get_cell_score( cell_x, cell_y )
        
        #change active cell
        newcell = (x-cell_x*self.n, y-cell_y*self.n)
        if self.get_cell_score(newcell[0], newcell[1]):
            self.active_cell = (None,None)
        else:
            self.active_cell = newcell
        # print(move, end="->")
        # print(self.active_cell)


