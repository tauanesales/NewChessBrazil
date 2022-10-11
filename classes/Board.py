from classes.Piece import Color

class Square:
  def __init__(self, square, x, y, width, height, piece = None):
    self.square = square
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.piece = piece
    self.status = 0

  def returnPoint(self, x, y): # retorna True se for clicado na casa
    return (self.x * self.width) <= x < (self.x + 1) * self.width \
        and (self.y * self.height) <= y < (self.y + 1) * self.height

  def returnCoordinates(self, x, y): # retorna as coordenadas da "matriz"
    if self.returnPoint(x, y):
      return self.x, self.y

  def hasPiece(self, x, y): # verifica se há peça nessa casa
    if self.returnPoint(x, y) and self.piece != None:
      return True

  def returnPieceColor(self): # retorna a cor da peça
    if self.piece != None:
      return self.piece.color

  def drawPiece(self): # desenhar a peça na janela
    if self.piece != None:
      return self.piece.image.draw()

  def squareColorChange(self, board): # mudança de cor no tabuleiro
    colors = [(255, 255, 255), (128, 128, 128)]
    moveList = self.pieceMoveList(board)
    if self.status == 0: # caso não esteja clicado
      self.status = 1
      self.square.color = (0, 0, 255)
      for square in moveList: # mudar a cor das casas que a peça pode mover
        (x, y) = square
        other_square = board[x+8*y]
        if self.analyseCapture(other_square): # caso haja alguma peça capturável
          other_square.square.color = (255, 0, 0)
        else:
          other_square.square.color = (128, 0, 0)
    else: # retorna a(s) casa(s) às cores originais
      self.status = 0
      self.square.color = colors[(self.x + self.y + 1) % 2]
      for square in moveList:
        (x, y) = square
        other_square = board[x + 8 * y]
        other_square.square.color = colors[(x + y + 1) % 2]

  def onClick(self, gamestate, board): # efetuar a mudança da cor do tabuleiro caso o turno atual condizer à cor
    if gamestate.whiteToMove == True and self.returnPieceColor() == Color.WHITE:
      self.squareColorChange(board)
      return True
    elif gamestate.whiteToMove == False and self.returnPieceColor() == Color.BLACK:
      self.squareColorChange(board)
      return True
    else:
      pass

  def pieceMoveList(self, board): # retorna a lista de movimentos possíveis da peça (lista de tuplas)
    return self.piece.moveList(board)

  def analyseMove(self, new_square, board): # verificar se é possível mover através da lista
    movelist = self.pieceMoveList(board)
    return self.piece.move(new_square, movelist)

  def changeImageCoord(self, xf, yf): # mudar coords da imagem
      self.piece.image.x = xf*self.width
      self.piece.image.y = yf*self.height

  def analyseCapture(self, new_square): # verificar captura (útil quando implantar xeques)
    return self.piece.capture(new_square)

  def movePiece(self, new_square, board): # mover a peça de casa, vincula-a a nova e desvincula da atual
    self.squareColorChange(board)
    self.piece.x = new_square.x
    self.piece.y = new_square.y
    new_square.piece = self.piece
    self.piece = None
