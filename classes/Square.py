from pyglet import graphics
from classes.Colors import Color

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

    def pieceMoveList(self, gamestate, board):  # retorna a lista de movimentos possíveis da peça (lista de tuplas)
        return self.piece.validMoves(gamestate, board)

    def analyseMove(self, new_square, gamestate, board):  # verificar se é possível mover através da lista
        movelist = self.pieceMoveList(gamestate, board)
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
    
    def updateCastlingRights(self,gamestate):
        
        if self.piece.ID == "K" and self.piece.color == Color.WHITE:

            gamestate.currentCastlingRight.whiteKingSide = False
            gamestate.currentCastlingRight.whiteQueenSide = False

        if self.piece.ID == "K" and self.piece.color == Color.BLACK:
            gamestate.currentCastlingRight.blackKingSide = False
            gamestate.currentCastlingRight.blackQueenSide = False


        if self.piece.ID == "R" and self.piece.color == Color.WHITE and self.j == gamestate.whiteKingPosition[1] - 4:
            gamestate.currentCastlingRight.whiteQueenSide = False

        if self.piece.ID == "R" and self.piece.color == Color.WHITE and self.j == gamestate.whiteKingPosition[1] + 3:
            gamestate.currentCastlingRight.whiteKingSide = False

        if self.piece.ID == "R" and self.piece.color == Color.BLACK and self.j == gamestate.blackKingPosition[1] - 4:
            gamestate.currentCastlingRight.blackQueenSide = False

        if self.piece.ID == "R" and self.piece.color == Color.BLACK and self.j == gamestate.blackKingPosition[1] + 3:
            gamestate.currentCastlingRight.blackKingSide = False

    
    def movePiece(self, new_square, board, gamestate):  # mover a peça de casa, vincula-a a nova e desvincula da atual
        
        if self.piece.ID == "K" and new_square.j - self.piece.j  == 2:
            gamestate.getKingSideCastleMoves(board)

        elif self.piece.ID == "K" and self.piece.j - new_square.j  == 2:
            gamestate.getQueenSideCastleMoves(board)
        else:
        
            self.piece.i = new_square.i
            self.piece.j = new_square.j
        
            if self.piece.ID == "K" and self.piece.color == Color.WHITE:
                gamestate.whiteKingPosition = (new_square.i,new_square.j)
        

            if self.piece.ID == "K" and self.piece.color == Color.BLACK:
                gamestate.blackKingPosition = (new_square.i,new_square.j)

            self.updateCastlingRights(gamestate)

            new_square.piece = self.piece
            self.piece = None
            new_square.changeImageCoord()
            new_square.piece.validMoves(gamestate,board)

            if new_square.piece.ID == "p":
                new_square.piece.promotePawn(board)

        gamestate.getAllEnemyValidMoves(board)
        print(gamestate.checkMate)

    def capturePiece(self, new_square, board):
        return self.piece.capture(new_square, board)
