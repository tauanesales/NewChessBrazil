from classes.Piece import Color

class Square:
  def __init__(self, square, i, j, width, height, piece = None):
    self.square = square
    self.i = i
    self.j = j
    self.width = width
    self.height = height
    self.piece = piece # pode conter peça ou não
    self.status = 0

  def returnPoint(self, x, y): # retorna True se for clicado na casa
    return (self.i * self.width) <= y < (self.i + 1) * self.width \
        and (self.j * self.height) <= x < (self.j + 1) * self.height

  def returnCoordinates(self): # retorna as coordenadas da "matriz"
    return self.i, self.j

  def hasPiece(self, i, j): # verifica se há peça nessa casa
    if self.returnPoint(i, j) and self.piece != None:
      return True

  def returnPieceColor(self): # retorna a cor da peça
    if self.piece != None:
      return self.piece.color

  def drawPiece(self): # desenhar a peça na janela
    if self.piece != None:
      return self.piece.image.draw()

  def squareColorChange(self, board): # mudança de cor no tabuleiro
    colors = [(255, 255, 255), (128, 128, 128)]
    actual_i, actual_j = self.returnCoordinates()
    moveList = self.pieceMoveList(board)
    if self.status == 0: # caso não esteja clicado
      self.status = 1
      self.square.color = (0, 0, 255)
      for coord in moveList: # mudar a cor das casas que a peça pode mover
        (i, j) = coord
        other_square = board[i][j]
        if self.analyseCapture(other_square): # caso haja alguma peça capturável
          other_square.square.color = (255, 0, 0)
        else:
          other_square.square.color = (128, 0, 0)
    else: # retorna a(s) casa(s) às cores originais
      self.status = 0
      self.square.color = colors[(self.i + self.j + 1) % 2]
      for square in moveList:
        (i, j) = square
        other_square = board[i][j]
        actual_square = board[actual_i][actual_j]
        other_square.square.color = colors[(i + j + 1) % 2]
        if type(actual_square.piece).__name__ == "Pawn": # mudança da cor da segunda casa do peão, sujeito a alterações
          piece = actual_square.piece
          if piece.color == Color.WHITE and board[actual_i+2][actual_j].square.color != colors[(i + j + 1) % 2]:
            board[actual_i+2][actual_j].square.color = colors[(actual_i + actual_j + 2 + 1) % 2]
          elif piece.color == Color.BLACK and board[actual_i-2][actual_j].square.color != colors[(i + j + 1) % 2]:
            board[actual_i-2][actual_j].square.color = colors[(actual_i + actual_j + 2 + 1) % 2]


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

  def changeImageCoord(self, i_final, j_final): # mudar coords da imagem
      self.piece.image.x = j_final*self.width
      self.piece.image.y = i_final*self.height

  def analyseCapture(self, new_square): # verificar captura (útil quando implantar xeques)
    return self.piece.capture(new_square)

  def movePiece(self, new_square, board): # mover a peça de casa, vincula-a a nova e desvincula da atual
    self.squareColorChange(board)
    self.piece.i = new_square.i
    self.piece.j = new_square.j
    new_square.piece = self.piece
    self.piece = None
