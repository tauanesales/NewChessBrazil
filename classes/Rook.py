import Piece

class Rook(Piece):
  def __init__(self,x,y,color):
    super().__init__(x,y,color)
    
    if color == "white":
      self.representation = "wR"
    else:
      self.representation = "bR"
    
  def move(self):
    pass