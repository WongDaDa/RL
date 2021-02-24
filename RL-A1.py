#!/usr/bin/env python
# coding: utf-8

# In[41]:


import copy


# In[1]:


import numpy as np


# In[2]:


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


# In[48]:


class Node:
    
    def __init__(self,initType=None,initName=None,initBoard=None,parent=None):
        self.nodeType = initType
        self.nodeName = initName
        self.parent = parent
        self.board = initBoard
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
    
    def setNodeParent(self,parent):
        self.parent = parent
        
    def getNodeParent(self):
        return self.parent
    
    def setNodeBoard(self,board):
        self.board = board
        
    def getNodeBoard(self):
        return self.board
        
    


# In[4]:


def evaluation():
    return np.randint(0,10)


# In[24]:


INF = 999
def Alphabeta(node,alpha,beta,depth):
    if depth <= 0:
        return evaluation(node)
    elif node.getNodeType() == 'MAX':
        g = -INF
        for child in node.getNodeChildren():
            g = max(g, Alphabeta(child,alpha,beta,depth-1))
            alpha = max(alpha,g)
            if alpha>=beta:
                break
    elif node.getNodeType == 'MIN':
        g = INF
        for child in node.getNodeChildren():
            g = min(g, Alphabeta(child,alpha,beta,depth-1))
            beta = min(beta.g)
            if alpha >=beta:
                break
    return g


# In[63]:


board = HexBoard(11)


# In[64]:


def getKeys(d, val):
    return [k for k,v in d.items() if v == val]


# In[98]:


root = Node('MAX',(11,0))


# In[92]:


def TreeGeneratorWithBoard(node,depth,player):
    if depth > 0:
        current_status = node.getNodeBoard()
        legalMoves = getKeys(current_status,3)
        for move in legalMoves:
            newBoard = copy.deepcopy(current_status)
            newBoard[move] = player
            if depth%2 == 0:
                nodeType = 'MAX'
                next_player = HexBoard.BLUE
            else:
                nodeType = 'MIN'
                next_player = HexBoard.RED
            newChild = Node(initType=nodeType,initName=move,initBoard=newBoard,parent=node)
            TreeGenerator(newChild,depth-1,next_player)
            node.addNodeChild(newChild)


# In[129]:


def TreeGeneratorWithLoc(node,status,depth,player):
    if depth > 0:
        for move in status:
            if depth%2 == 0:
                nodeType = 'MAX'
                next_player = HexBoard.BLUE
            else:
                nodeType = 'MIN'
                next_player = HexBoard.RED
            newChild = Node(initType=nodeType,initName=move,parent=node)
            newStatus = copy.deepcopy(status)
            newStatus.remove(move)
            TreeGenerator(newChild,newStatus,depth-1,next_player)
            node.addNodeChild(newChild)


# In[130]:


status = getKeys(board.board,3)
TreeGenerator(root,status,3,HexBoard.RED)


# In[134]:


sys.getsizeof(c)


# In[135]:


c = root.getNodeChildren()[0].getNodeChildren()[0].getNodeChildren()[0]


# In[136]:


c


# In[ ]:




