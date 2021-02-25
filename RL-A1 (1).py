#!/usr/bin/env python
# coding: utf-8

# In[1]:


import copy


# In[2]:


import numpy as np


# In[189]:


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
        
    def getLegalMove(self):
        return [k for k,v in self.board.items() if v == HexBoard.EMPTY]


# In[190]:


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


# In[221]:


def evaluation(status):
    return np.random.randint(-998,998)


# In[ ]:


def evaluationShortestPath(status):


# In[222]:


INF = 999
def Alphabeta(status,alpha,beta,depth,maximizingPlayer):
    if depth <= 0:
        return evaluation(status)
    
    if maximizingPlayer:
        g = -INF
        legalMoves = getKeys(status,HexBoard.EMPTY)
        for move in legalMoves:
            childStatus = copy.deepcopy(status)
            childStatus[move] = HexBoard.RED
            g = max(g, Alphabeta(childStatus,alpha,beta,depth-1,False))
            alpha = max(alpha,g)
            if alpha>=beta:
                break
    else:
        g = INF
        legalMoves = getKeys(status,HexBoard.EMPTY)
        for move in legalMoves:
            childStatus = copy.deepcopy(status)
            childStatus[move] = HexBoard.BLUE
            g = min(g, Alphabeta(childStatus,alpha,beta,depth-1,True))
            beta = min(beta,g)
            if alpha >=beta:
                break
    return g


# In[223]:


def getNextMove(board,maximizingPlayer):
    result = []
    moveList = board.getLegalMove()
    for move in moveList:
        status = copy.deepcopy(board.board)
        if maximizingPlayer:
            status[move]=HexBoard.BLUE
        else:
            status[move]=HexBoard.RED
        result.append(Alphabeta(status,-INF,INF,3,player))
    select = np.argmax(result)
    return moveList[select]


# In[226]:


newBoard = HexBoard(7)


# In[227]:


while not newBoard.is_game_over():
    move_minimizing = getNextMove(newBoard,False)
    newBoard.place(move_minimizing,HexBoard.BLUE)
    move_maximizing = getNextMove(newBoard,True)
    newBoard.place(move_maximizing,HexBoard.RED)
    newBoard.print()


# #END
