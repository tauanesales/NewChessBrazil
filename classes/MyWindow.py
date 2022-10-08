import pyglet
from classes.Piece import Peca

class MyWindow(pyglet.window.Window):
  def __init__(self, width, height, board, pieces, running, gamestate):
    super().__init__(width, height, caption = "Chess")
    self.board = board
    self.pieces = pieces
    self.running = running
    self.gamestate = gamestate

  def on_draw(self):
    
    if self.running:

      self.clear()

      for rect in self.board:
        rect.forma.draw()

      for piece in self.pieces:
        piece.image.draw()
    

  def on_mouse_press(self, x, y, button, modifiers):

    if self.gamestate.clicado == 0:

      for piece in self.pieces:

        if piece.clica(x, y, self.gamestate, self.board):
          self.gamestate.clicado = 1

    else:
      for rect in self.board:
        if rect.clicou_na_casa(x, y):
          xf, yf = rect.retornar_coord(x, y)

      for piece in self.pieces:
        if piece.mover(xf, yf, self.gamestate, self.board):
          self.gamestate.mudarTurno()
        else:
          if piece.status == 1:
            piece.mudanca_tabuleiro(self.board)
      self.gamestate.clicado = 0
