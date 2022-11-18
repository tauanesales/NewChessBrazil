from pyglet import graphics

class Square:
    def __init__(self, square, i, j, width, height, piece=None):
        self.square = square
        self.i = i
        self.j = j
        self.width = width
        self.height = height
        self.piece = piece  # pode conter peça ou não
        self.status = 0
        self.o_color = self.square.color

    @property
    def color(self):
        return self.square.color

    @color.setter
    def color(self, other):
        self.square.color = other

    def returnPoint(self, x, y):  # retorna True se for clicado na casa
        return (self.i * self.width) <= y < (self.i + 1) * self.width \
               and (self.j * self.height) <= x < (self.j + 1) * self.height

    def returnCoordinates(self, x, y):  # retorna as coordenadas da "matriz"
        return self.i, self.j

    def returnPieceColor(self):  # retorna a cor da peça
        if self.piece is not None:
            return self.piece.color

    def drawPiece(self):  # desenhar a peça na janela
        if self.piece is not None:
            return self.piece.image.draw()

    def pieceMoveList(self, board, rotation):  # retorna a lista de movimentos possíveis da peça (lista de tuplas)
        
        return self.piece.moveList(board, rotation)

    def analyseMove(self, new_square, board, rotation):  # verificar se é possível mover através da lista
        movelist = self.pieceMoveList(board, rotation)
        return self.piece.move(new_square, movelist)

    def changeImageCoord(self, xf = None, yf = None):  # mudar coords da imagem
        if xf is None and yf is None:
            self.piece.image.x = self.j * self.width
            self.piece.image.y = self.i * self.height
        else:
            self.piece.image.x = xf
            self.piece.image.y = yf
            self.piece.image.group = graphics.OrderedGroup(1)

    def analyseCapture(self, new_square):  # verificar captura (útil quando implantar xeques)
        return self.piece.canCapture(new_square)

    def movePiece(self, new_square, board, gamestate):  # mover a peça de casa, vincula-a a nova e desvincula da atual
        self.piece.i = new_square.i
        self.piece.j = new_square.j
        new_square.piece = self.piece
        self.piece = None
        new_square.changeImageCoord()
        
        new_square.piece.isCheck(board,gamestate)
        print(gamestate.check)

    def capturePiece(self, new_square, board):
        return self.piece.capture(new_square, board)
