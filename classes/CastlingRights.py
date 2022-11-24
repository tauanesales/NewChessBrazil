class CastlingRights:

  def __init__(self,whiteKingSide,whiteQueenSide,blackKingSide,blackQueenSide):
    
    self.whiteKingSide = whiteKingSide
    self.whiteQueenSide = whiteQueenSide
    self.blackKingSide = blackKingSide
    self.blackQueenSide = blackQueenSide
    
    
  def __repr__(self) -> str:
    
    return  f"({self.whiteKingSide},{self.whiteQueenSide},{self.blackKingSide},{self.blackQueenSide})"