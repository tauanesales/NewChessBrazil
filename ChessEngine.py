""""
This class is responsible for storing all the information about the current state of a chess game. It also be responsible for determining the valid moves at the current state. It will also keep a move log
"""

class  GameState():
  
  # we could use numpy array to turn more efficient and more compatible with AI
  # the  first caracter of the piece is the color of it and the second is the type
  def __init__(self):
    self.board = [
      ["bR","bN","bB","bQ","bK","bB","bN","bR"],
      ["bp","bp","bp","bp","bp","bp","bp","bp"],
      ["--","--","--","--","--","--","--","--"],
      ["--","--","--","--","--","--","--","--"],
      ["--","--","--","--","--","--","--","--"],
      ["--","--","--","--","--","--","--","--"],
      ["wp","wp","wp","wp","wp","wp","wp","wp"],
      ["wR","wN","wB","wQ","wK","wB","wN","wR"],
    ]
    self.witheToMove = True
    self.moveLog = []