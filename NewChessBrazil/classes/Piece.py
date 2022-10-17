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

  def move(self, new_square, movelist): # verifica se na lista de movimentos é possível mover a peça à casa desejada
    for i in movelist: # movelist = lista de tuplas, logo i = tupla
      (x, y) = i
      if (x, y) == (new_square.x, new_square.y):
        return True

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

  def move(self, new_square, movelist):
    for i in movelist: # movelist = lista de tuplas, logo i = tupla
      (x, y) = i
      if (x, y) == (new_square.x, new_square.y):
        return True

  def moveList(self, board): # flexível para torres, bispos e rainhas
    moveList = []
    directions = 0
    possible_moves = [1, 1, 1, 1]
    while directions < 4:
      if directions == 0:
        (xf, yf) = (self.x + possible_moves[directions], self.y)
      elif directions == 1:
        (xf, yf) = (self.x, self.y + possible_moves[directions])
      elif directions == 2:
        (xf, yf) = (self.x - possible_moves[directions], self.y)
      else:
        (xf, yf) = (self.x, self.y - possible_moves[directions])
      possible_moves[directions] += 1
      if self.isInRange(xf, yf): # verificar se as coords finais estão dentro da matriz
        if board[xf+yf*8].piece == None: # verificar se a peça é da mesma cor
          moveList.append((xf, yf)) # append de uma tupla
        elif board[xf+yf*8].returnPieceColor() != self._color:
          moveList.append((xf, yf))
          directions += 1
        else:
          directions += 1
      else:
        directions += 1
    return moveList

class Knight(Piece):
  def __init__(self, image, id, width, height, x, y):
    super().__init__(image, id, width, height, x, y)

  def moveList(self, board): # lista de movimentos
    moveList = []
    possible_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)] # melhorar o entendimento
    for move in possible_moves:
      (xf, yf) = (self.x + move[0], self.y + move[1])
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
  
  def move(self, new_square, movelist): # verifica se na lista de movimentos é possível mover a peça à casa desejada
    for i in movelist: # movelist = lista de tuplas, logo i = tupla
      (x, y) = i
      if (x, y) == (new_square.x, new_square.y):
        return True

  def moveList(self, board):
    movelist = []
    possible_move = [1, 1, 1, 1] # [1º quadrante, 2º quad, 3º quad, 4º quad]
    directions = 0
    while directions < 4:
      if directions == 0:
        xf, yf = self.x + possible_move[directions], self.y + possible_move[directions]
      elif directions == 1:
        xf, yf = self.x - possible_move[directions], self.y + possible_move[directions]
      elif directions == 2:
        xf, yf = self.x - possible_move[directions], self.y - possible_move[directions]
      else:
        xf, yf = self.x + possible_move[directions], self.y - possible_move[directions]
      possible_move[directions] += 1
      
      if self.isInRange(xf, yf):
        if board[xf + 8*yf].piece == None:
          movelist.append((xf, yf))
        elif board[xf + 8*yf].returnPieceColor() == self._color:
          directions += 1
        else:
          movelist.append((xf, yf))
          directions += 1
      else:
        directions += 1
    return movelist

class Queen(Piece):
  def __init__(self, image, id, width, height, x, y):
    super().__init__(image, id, width, height, x, y)

  def move(self, new_square, movelist): # verifica se na lista de movimentos é possível mover a peça à casa desejada
    for i in movelist: # movelist = lista de tuplas, logo i = tupla
      (x, y) = i
      if (x, y) == (new_square.x, new_square.y):
        return True
        
  def moveList(self, board):
    movelist = []
    movelist += Rook.moveList(self, board)
    movelist += Bishop.moveList(self, board)
    return movelist

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