from abc import ABC, abstractmethod

class Peca(ABC):
  def __init__(self, image, id, x, y, width, height):
    self.image = image
    self.id = id
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.status = 0

  def contem_ponto(self, x, y):
      return (self.x*self.width) <= x < (self.x+1)*self.width \
          and (self.y*self.height) <= y < (self.y+1)*self.height

  def mudanca_tabuleiro(self, board):
    cores = [(255, 255, 255), (128, 128, 128)]
    if self.status == 0:
      self.status = 1
      board[self.x * 8 + self.y].forma.color = (0, 0, 255)
    else:
      self.status = 0
      board[self.x * 8 + self.y].forma.color = cores[(self.x + self.y + 1) % 2]

  def on_click(self, gamestate, board):
    if gamestate.whiteToMove == True and self.id[0] == "w":
      self.mudanca_tabuleiro(board)
      return True
    elif gamestate.whiteToMove == False and self.id[0] == "b":
      self.mudanca_tabuleiro(board)
      return True
    else:
      pass

  def clica(self, x, y, gamestate, board):
    if self.contem_ponto(x, y) and self.on_click(gamestate, board):
      return True


  @abstractmethod
  def mover(self, xf, yf, gamestate, board):
    pass

  def capturar(self):
    if board[self.x_final][self.x_final] != "--": # capturar
      pass

  def analise_check(self):
    pass

class Torre(Peca):
  def __init__(self, image, id, x, y, width, height):
    super().__init__(image, id, x, y, width, height)

  def mover(self, xf, yf, gamestate, board):
    if self.status == 1:
      print("Rook")


class Cavalo(Peca):
  def __init__(self, image, id, x, y, width, height):
    super().__init__(image, id, x, y, width, height)

  def mover(self, xf, yf, gamestate, board):
    if self.status == 1:
      if (abs(xf-self.x) == 1 and abs(yf-self.y) == 2) or (abs(yf-self.y) == 1 and abs(xf-self.x) == 2):
        if gamestate.board[7-yf][xf][0] != self.id[0]:
          self.mudanca_tabuleiro(board)
          self.x, self.y = xf, yf
          self.image.x, self.image.y = self.x*self.width, self.y*self.height
          return True

class Bispo(Peca):
  def __init__(self, image, id, x, y, width, height):
    super().__init__(image, id, x, y, width, height)

  def mover(self, xf, yf, gamestate, board):
    if self.status == 1:
      print("Bishop")

class Rainha(Peca):
  def __init__(self, image, id, x, y, width, height):
    super().__init__(image, id, x, y, width, height)

  def mover(self, xf, yf, gamestate, board):
    if self.status == 1:
      print("Queen")

class Rei(Peca):
  def __init__(self, image, id, x, y, width, height):
    super().__init__(image, id, x, y, width, height)

  def mover(self, xf, yf, gamestate, board):
    if self.status == 1:
      print("King")

class Peao(Peca):
  def __init__(self, image, id, x, y, width, height):
    super().__init__(image, id, x, y, width, height)

  def mover(self, xf, yf, gamestate, board):
    if self.status == 1:
      print("Pawn")
