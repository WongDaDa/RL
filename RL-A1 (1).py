#!/usr/bin/env python
# coding: utf-8

# In[1]:


import copy


# In[2]:


import numpy as np


# In[3]:


import time


# In[4]:


class HexBoard:
    BLUE = 1
    RED = 2
    EMPTY = 3
    def __init__(self, board_size):
        self.board = {}
        self.size = board_size
        self.game_over = False
        for x in range(board_size):
            for y in range (board_size):
                self.board[x,y] = HexBoard.EMPTY
    def is_game_over(self):
        return self.game_over
    def is_empty(self, coordinates):
        return self.board[coordinates] == HexBoard.EMPTY
    def is_color(self, coordinates, color):
        return self.board[coordinates] == color
    def get_color(self, coordinates):
        if coordinates == (-1,-1):
            return HexBoard.EMPTY
        return self.board[coordinates]
    def place(self, coordinates, color):
        if not self.game_over and self.board[coordinates] == HexBoard.EMPTY:
            self.board[coordinates] = color
        if self.check_win(HexBoard.RED) or self.check_win(HexBoard.BLUE):
            self.game_over = True
    def get_opposite_color(self, current_color):
        if current_color == HexBoard.BLUE:
            return HexBoard.RED
        return HexBoard.BLUE
    def get_neighbors(self, coordinates):
        (cx,cy) = coordinates
        neighbors = []
        if cx-1>=0:   neighbors.append((cx-1,cy))
        if cx+1<self.size: neighbors.append((cx+1,cy))
        if cx-1>=0    and cy+1<=self.size-1: neighbors.append((cx-1,cy+1))
        if cx+1<self.size  and cy-1>=0: neighbors.append((cx+1,cy-1))
        if cy+1<self.size: neighbors.append((cx,cy+1))
        if cy-1>=0:   neighbors.append((cx,cy-1))
        return neighbors
    def border(self, color, move):
        (nx, ny) = move
        return (color == HexBoard.BLUE and nx == self.size-1) or (color == HexBoard.RED and ny == self.size-1)
    def traverse(self, color, move, visited):
        if not self.is_color(move, color) or (move in visited and visited[move]): return False
        if self.border(color, move): return True
        visited[move] = True
        for n in self.get_neighbors(move):
            if self.traverse(color, n, visited): return True
        return False
    def check_win(self, color):
        for i in range(self.size):
            if color == HexBoard.BLUE: move = (0,i)
            else: move = (i,0)
            if self.traverse(color, move, {}):
                return True
        return False
    def print(self):
        print("   ",end="")
        for y in range(self.size):
            print(chr(y+ord('a')),"",end="")
        print("")
        print(" -----------------------")
        for y in range(self.size):
            print(y, "|",end="")
            for z in range(y):
                print(" ", end="")
            for x in range(self.size):
                piece = self.board[x,y]
                if piece == HexBoard.BLUE: print("b ",end="")
                elif piece == HexBoard.RED: print("r ",end="")
                else:
                    if x==self.size:
                        print("-",end="")
                    else:
                        print("- ",end="")
            print("|")
        print("   -----------------------")


# In[5]:


def getLegalMove(status):
    return [k for k,v in status.items() if v == HexBoard.EMPTY]


# In[6]:


class Node:
    def __init__(self,initType=None,initName=None):
        self.nodeType = initType
        self.nodeName = initName
        self.children = []
        
    def setNodeType(self,nodeType):
        self.nodeType = nodeType
        
    def getNodeType(self):
        return self.nodeType
    
    def setNodeName(self,nodeName):
        self.nodeName = nodeName
    
    def getNodeName(self):
        return self.nodeName
    
    def setNodeChild(self,children):
        self.children = children
        
    def addNodeChild(self,child):
        self.children.append(child)
        
    def getNodeChildren(self):
        return self.children


# In[7]:


def evaluation(status):
    return np.random.randint(-998,998)


# In[8]:


INF = 999
def Alphabeta(status,alpha,beta,depth,maximizingPlayer):
    if depth <= 0:
        return evaluationShortestPath(boardSize,status)
    
    if maximizingPlayer:
        g = -INF
        legalMoves = getLegalMove(status)
        for move in legalMoves:
            childStatus = copy.deepcopy(status)
            childStatus[move] = HexBoard.RED
            g = max(g, Alphabeta(childStatus,alpha,beta,depth-1,False))
            alpha = max(alpha,g)
            if alpha>=beta:
                break
    else:
        g = INF
        legalMoves = getLegalMove(status)
        for move in legalMoves:
            childStatus = copy.deepcopy(status)
            childStatus[move] = HexBoard.BLUE
            g = min(g, Alphabeta(childStatus,alpha,beta,depth-1,True))
            beta = min(beta,g)
            if alpha >=beta:
                break
    return g


# In[9]:


def getNextMove(status,maximizingPlayer,depth):
    result = []
    moveList = getLegalMove(status)
    for move in moveList:
        newStatus = copy.deepcopy(status)
        if maximizingPlayer:
            newStatus[move]=HexBoard.BLUE
        else:
            newStatus[move]=HexBoard.RED
        result.append(Alphabeta(newStatus,-INF,INF,depth,maximizingPlayer))
    select = np.argmax(result)
    return moveList[select]


# In[10]:


def status_to_matrix(size, status, color):
    a = status
    b = list(a)
    if color == HexBoard.BLUE:
        status_matrix = np.zeros([size,size+2])
        for item in b:
            x = item[0]
            y = item[1]
            if a[item] == color:
                status_matrix[x,y+1] = 0
            elif a[item] == HexBoard.EMPTY:
                status_matrix[x,y+1] = 1
            else:
                status_matrix[x,y+1] = 999
        return status_matrix.T
    else:
        status_matrix1 = np.zeros([size+2,size])
        for item in b:
            x = item[0]
            y = item[1]
            if a[item] == color:
                status_matrix1[x+1,y] = 0
            elif a[item] == HexBoard.EMPTY:
                status_matrix1[x+1,y] = 1
            else:
                status_matrix1[x+1,y] = 999
        return status_matrix1


# In[11]:


def search_neighbor(matrix,position):
    x=position[0]
    y=position[1]
    if y>0:
        neighbor = [(x,y-1),(x+1,y-1),(x+1,y)]
        value = [matrix[x,y-1],matrix[x+1,y-1],matrix[x+1,y]]
        score = min(value)
        index = value.index(score)
        return score, negihbor[index]
    else:
        return matrix[x+1,y],(x+1,y)

def evaluationShortestPath(size,status):
    matrix = status_to_matrix(status)
    start = (0,size-1)
    all_score = 0
    move_list = []
    while(x<4):
        score, start = search_neighbor(matrix,start)
        all_score = all_score + score
        #move_list.append(start)
    return all_score


# In[31]:


def AlphabetaTT(move,board,alpha,beta,depth,maximizingPlayer,TT):
    bestMove = []
    for item in TT:
        if board.board in item:
            bestMove = item[3]
            if item[1] >= depth:
                print('pruning')
                return item[2]
        else:
            bestMove = []
    
    if depth <= 0:
        g = evaluation(board.board)
        return g
    
    elif maximizingPlayer:
        g = -INF
        legalMoves = getLegalMove(board.board)
        for move in bestMove+legalMoves:
            childStatus = copy.deepcopy(board)
            childStatus.board[move] = HexBoard.RED
            gc = AlphabetaTT(move,childStatus,alpha,beta,depth-1,False,TT)
            if gc > g:
                bestMove = move
                g = gc
            alpha = max(alpha,g)
            if alpha>=beta:
                TT.append(board.board,depth,g,bestMove)
                break
    elif not maximizingPlayer:
        g = INF
        legalMoves = bestMove+getLegalMove(board.board)
        for move in legalMoves:
            childStatus = copy.deepcopy(board)
            childStatus.board[move] = HexBoard.BLUE
            gc = AlphabetaTT(move,childStatus,alpha,beta,depth-1,False,TT)
            if gc < g:
                bestMove = move
                g = gc
            beta = min(beta,g)
            if alpha >=beta:
                TT.append((board.board,depth,g,bestMove))
                break
    return g


# In[32]:


#Iterative Deepening with Alphabeta_TT
def getNextMoveWithID(board,maximizingPlayer):
    TT = []
    startTime = time.time()
    depth = 1
    select = 0
    while time.time() - startTime < 30:
        result = []
        moveList = getLegalMove(board.board)
        for move in moveList:
            newStatus = copy.deepcopy(board)
            if maximizingPlayer:
                newStatus.board[move]=HexBoard.BLUE
            else:
                newStatus.board[move]=HexBoard.RED
            result.append(AlphabetaTT(move,newStatus,-INF,INF,depth,maximizingPlayer,TT))
        select = np.argmax(result)
        depth += 1
        print('current depth: {}'.format(depth))
    return moveList[select]


# In[33]:


board = HexBoard(6)


# In[34]:


while board.is_game_over:
    move = getNextMoveWithID(board,True)
    board.place(move,HexBoard.RED)
    move = getNextMoveWithID(board,False)
    board.place(move,HexBoard.BLUE)
    board.print()


# In[ ]:




