from classes.Colors import Color, sColor


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

    def returnCoordinates(self):  # retorna as coordenadas da "matriz"
        return self.i, self.j

    def hasPiece(self, i, j):  # verifica se há peça nessa casa
        if self.returnPoint(i, j) and self.piece != None:
            return True

    def returnPieceColor(self):  # retorna a cor da peça
        if self.piece is not None:
            return self.piece.color

    def drawPiece(self):  # desenhar a peça na janela
        if self.piece is not None:
            return self.piece.image.draw()

    def squareColorChange(self, board, rotation):  # mudança de cor no tabuleiro
        moveList = self.pieceMoveList(board, rotation)

        if self.status == 0:  # caso não esteja clicado
            self.status = 1
            self.color = sColor.CLICKED.value

            for coord in moveList:  # mudar a cor das casas que a peça pode mover
                (i, j) = coord
                other_square = board[i][j]

                if self.analyseCapture(other_square):  # caso haja alguma peça capturável
                    other_square.color = sColor.CAPTURE.value

                else:
                  if other_square.o_color == sColor.WHITE.value:
                    other_square.color = sColor.MOVEMENT.value

                  else:
                    other_square.color = sColor.MOVEMENT2.value

        else:  # retorna a(s) casa(s) às cores originais
            self.status = 0
            self.color = self.o_color
            self.reverseBoardColor(board)

    def reverseBoardColor(self, board):
        for line in board:
            for square in line:
                if square.color != square.o_color:
                    square.color = square.o_color

    def onClick(self, gamestate, board):  # efetuar a mudança da cor do tabuleiro caso o turno atual condizer à cor
        if gamestate.whiteToMove == True and self.returnPieceColor() == Color.WHITE:
            self.squareColorChange(board, gamestate.rotation)
            return True

        elif gamestate.whiteToMove == False and self.returnPieceColor() == Color.BLACK:
            self.squareColorChange(board, gamestate.rotation)
            return True

    def pieceMoveList(self, board, rotation):  # retorna a lista de movimentos possíveis da peça (lista de tuplas)
        return self.piece.moveList(board, rotation)

    def analyseMove(self, new_square, board, rotation):  # verificar se é possível mover através da lista
        movelist = self.pieceMoveList(board, rotation)
        return self.piece.move(new_square, movelist)

    def changeImageCoord(self):  # mudar coords da imagem
        self.piece.image.x = self.j * self.width
        self.piece.image.y = self.i * self.height

    def analyseCapture(self, new_square):  # verificar captura (útil quando implantar xeques)
        return self.piece.canCapture(new_square)

    def movePiece(self, new_square, board, rotation):  # mover a peça de casa, vincula-a a nova e desvincula da atual
        self.squareColorChange(board, rotation)
        self.piece.i = new_square.i
        self.piece.j = new_square.j
        new_square.piece = self.piece
        self.piece = None
        new_square.changeImageCoord()
