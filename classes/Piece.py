from abc import ABC, abstractmethod
from enum import Enum

class Color(Enum): # uso do enum para as cores
  WHITE = 1
  BLACK = 2

class Piece(ABC):
  def __init__(self, image, id, width, height, x, y):
    self.image = image
    self.id = id
    self.width = width
    self.height = height
    if self.id[0] == "w":
      self._color = Color.WHITE
    else:
      self._color = Color.BLACK
    self.x = x
    self.y = y

  @property
  def color(self):
    return self._color

  @abstractmethod
  def move(self, new_square, old_square):
    pass

  @abstractmethod
  def moveList(self, board):
    pass

  def capture(self, new_square): # método de captura, não precisa verificar a cor, já implantado no move
    if self.move and new_square.piece != None:
      return True

  def isInRange(self, x, y): # caso a peça esteja dentro dos parâmetros, para não usar try para tratar erros
    if 0 <= x <= 7 and 0 <= y <= 7:
      return True

class Rook(Piece):
  def __init__(self, image, id, width, height, x, y):
    super().__init__(image, id, width, height, x, y)

  def move(self, new_square, movelist): # verifica se na lista de movimentos é possível mover a peça à casa desejada
    for i in movelist: # movelist = lista de tuplas, logo i = tupla
      (x, y) = i
      if (x, y) == (new_square.x, new_square.y):
        return True

  def moveList(self, board):
    moveList = []
    possible_indexes = [(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(1,0), 
    (2,0),(3,0),(4,0),(5,0),(6,0), (7,0),(8,0)]
    for i in possible_indexes:
      xf = self.x + i[0]
      yf = self.y + i[1]
      if self.isInRange(xf, yf): # verificar se as coords finais estão dentro da matriz
        if board[xf+yf*8].returnPieceColor() != self._color: # verificar se a peça é da mesma cor
          moveList.append((xf, yf)) # append de uma tupla
    return moveList


class Knight(Piece):
  def __init__(self, image, id, width, height, x, y):
    super().__init__(image, id, width, height, x, y)
    
  def moveList(self, board): # lista de movimentos
    moveList = []
    possible_indexes = [1, -1, 2, -2] # lista para iteração
    for i in possible_indexes:
      for j in possible_indexes:
        if abs(i) != abs(j): # cavalo move 2 casas verticais e 1 horizontal/2 horizontais e 1 vertical
          xf = self.x + i
          yf = self.y + j
          if self.isInRange(xf, yf): # verificar se as coords finais estão dentro da matriz
            if board[xf+yf*8].returnPieceColor() != self._color: # verificar se a peça é da mesma cor
              moveList.append((xf, yf)) # append de uma tupla
    return moveList

  def move(self, new_square, movelist): # verifica se na lista de movimentos é possível mover a peça à casa desejada
    for i in movelist: # movelist = lista de tuplas, logo i = tupla
      (x, y) = i
      if (x, y) == (new_square.x, new_square.y):
        return True

class Bishop(Piece):
  def __init__(self, image, id, width, height, x, y):
    super().__init__(image, id, width, height, x, y)

  def move(self, new_square, old_square):
    print("Bishop")

  def moveList(self, board):
    return []

class Queen(Piece):
  def __init__(self, image, id, width, height, x, y):
    super().__init__(image, id, width, height, x, y)

  def move(self, new_square, old_square):
    print("Queen")

  def moveList(self, board):
    return []

class King(Piece):
  def __init__(self, image, id, width, height, x, y):
    super().__init__(image, id, width, height, x, y)

  def move(self, new_square, old_square):
    print("King")

  def moveList(self, board):
    return []

class Pawn(Piece): 
  def __init__(self, image, id, width, height, x, y):
    super().__init__(image, id, width, height, x, y)
    self.already_moved = False

  def move(self, new_square, moveList):
    
    ans = True
    for i in moveList:
        
        if i == (new_square.x,new_square.y):

            
            if  i == (self.x,self.y - 2) and self.already_moved:
                self.already_moved = True
                ans = False
             
            if i == (self.x,self.y + 2) and self.already_moved:
                self.already_moved = True
                ans = False
            return ans
        

  def moveList(self, board):
      moveList = []
      possible_moves = [(0, 1), (0, 2),(0,-1),(0,-2)]

      for move in possible_moves:
          xf = self.x + move[0]
          yf = self.y + move[1] 

          if self.isInRange(xf, yf):
              # verificar se a peça é da mesma cor
              if board[xf+yf*8].returnPieceColor() != self._color:
                  moveList.append((xf, yf)) # append de uma tupla
      return moveList