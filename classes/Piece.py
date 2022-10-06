from abc import ABC, abstractmethod

class Piece(ABC):
  def __init__(self,x,y,representation,color):
    self.x = x
    self.y = y
    self.possible_moves = []
    self.color = color
    

  @abstractmethod
  def move(self,direction):
    pass
    
