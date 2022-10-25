import pyglet
from classes.Square import Square
from classes.Piece import *
from classes.Colors import *
from random import choice

class Board:

    def __init__(self, width, height):
        self.board = []
        self.white_pieces = []
        self.black_pieces = []
        self.width = width
        self.height = height
        self.dimension = 8  # tabuleiro 8x8
        self.images = {}  # dict de sprites das peças
        self.batch = pyglet.graphics.Batch()  # batch para renderizar com mais eficiência
        self.sprites = []  # lista dos shapes da casa para renderização (batch)
        self.board_rotation = choice([False, True])

        self.loadImages()
        self.createPieces()

    @property
    def square_size(self):
        return self.height // self.dimension

    def loadImages(self):
        pieces = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR", "bp",
                  "wp", "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]

        for piece in pieces:
            self.images[piece] = pyglet.image.load("public/" + piece + ".png")

    def createBoard(self):  # criação do tabuleiro
        colors = [(255, 255, 255), (128, 128, 128)]  # cor branca e cinza, alternância

        for i in range(self.dimension):
            line = []

            for j in range(self.dimension):
                color = colors[(i + j + 1) % 2]  # escolha da cor baseado na soma de linhas e colunas
                rectangle = pyglet.shapes.Rectangle(x=self.square_size * j, y=self.square_size * i,
                                                    batch=self.batch, width=self.square_size,
                                                    height=self.square_size, color=color)
                self.sprites.append(rectangle)
                square = Square(rectangle, i, j, self.square_size, self.square_size)  # instância da casa
                line.append(square)  # adicionar à matriz

            self.board.append(line)

    def addPiece(self, id, i, j):
        sprite = pyglet.sprite.Sprite(self.images[id], x = self.square_size*j,
                                    y = self.square_size*i)

        return sprite, id, i, j

    def createPieces(self):  # inserção das peças, contidas na casa

        self.createBoard()
        pieces = []

        if self.board_rotation:
            i = 7
        else:
            i = 0

        rook_w1 = Rook(*self.addPiece("wR", i, 0))
        rook_w2 = Rook(*self.addPiece("wR", i, 7))

        knight_w1 = Knight(*self.addPiece("wN", i, 1))
        knight_w2 = Knight(*self.addPiece("wN", i, 6))

        bishop_w1 = Bishop(*self.addPiece("wB", i, 2))
        bishop_w2 = Bishop(*self.addPiece("wB", i, 5))

        queen_w = Queen(*self.addPiece("wQ", i, 3))

        king_w = King(*self.addPiece("wK", i, 4))

        column = [rook_w1, knight_w1, bishop_w1, queen_w, king_w, bishop_w2, knight_w2, rook_w2]
        self.white_pieces += column

        if self.board_rotation:
            i = 6

        else:
            i = 1

        for j in range(8):
            pawn_w = Pawn(*self.addPiece("wp", i, j))
            self.white_pieces.append(pawn_w)

        if self.board_rotation:
            i = 1

        else:
            i = 6

        # Black
        for j in range(8):
            pawn_b = Pawn(*self.addPiece("bp", i, j))
            self.black_pieces.append(pawn_b)

        if self.board_rotation:
            i = 0

        else:
            i = 7

        rook_b1 = Rook(*self.addPiece("bR", i, 0))
        rook_b2 = Rook(*self.addPiece("bR", i, 7))

        knight_b1 = Knight(*self.addPiece("bN", i, 1))
        knight_b2 = Knight(*self.addPiece("bN", i, 6))

        bishop_b1 = Bishop(*self.addPiece("bB", i, 2))
        bishop_b2 = Bishop(*self.addPiece("bB", i, 5))

        queen_b = Queen(*self.addPiece("bQ", i, 3))

        king_b = King(*self.addPiece("bK", i, 4))

        column = [rook_b1, knight_b1, bishop_b1, queen_b, king_b, bishop_b2, knight_b2, rook_b2]
        self.black_pieces += column

        pieces += self.white_pieces
        pieces += self.black_pieces

        for piece in pieces:
            i, j = piece.i, piece.j
            self.board[i][j].piece = piece

    def squareColorChange(self, i, j):  # mudança de cor no tabuleiro
        actual_square = self.board[i][j]
        moveList = actual_square.pieceMoveList(self.board, self.board_rotation)

        if actual_square.status == 0:  # caso não esteja clicado
            actual_square.status = 1
            actual_square.color = sColor.CLICKED.value

            for coord in moveList:  # mudar a cor das casas que a peça pode mover
                (old_i, old_j) = coord
                other_square = self.board[old_i][old_j]

                if actual_square.analyseCapture(other_square):  # caso haja alguma peça capturável
                    other_square.color = sColor.CAPTURE.value

                else:
                  if other_square.o_color == sColor.WHITE.value:
                    other_square.color = sColor.MOVEMENT.value

                  else:
                    other_square.color = sColor.MOVEMENT2.value

        else:  # retorna a(s) casa(s) às cores originais
            actual_square.status = 0
            actual_square.color = actual_square.o_color
            self.reverseBoardColor()

    def reverseBoardColor(self):
        for line in self.board:
            for square in line:
                
                if square.color != square.o_color:
                    square.color = square.o_color

    def pieceClick(self, x, y, shift):
        if shift:
            for piece in self.white_pieces:
                i, j = piece.i, piece.j
                if piece.returnPoint(x, y, self.square_size, self.square_size):
                    self.squareColorChange(i, j)
                    return (i, j)

        else:
            for piece in self.black_pieces:
                i, j = piece.i, piece.j
                if piece.returnPoint(x, y, self.square_size, self.square_size):
                    self.squareColorChange(i, j)
                    return (i, j)

        return 0

    def squareClick(self, x, y):
        i = j = None

        for line in self.board:
            for square in line:

                if square.returnPoint(x, y):
                    i, j = square.returnCoordinates(x, y)

        return i, j

    def isSameColor(self, i, j, old_i, old_j):
        new_square = self.board[i][j]
        old_square = self.board[old_i][old_j]

        if new_square.returnPieceColor() == None:
            return None

        elif new_square.returnPieceColor() == old_square.returnPieceColor():
            return True

        else:
            return False

    def noColorClick(self, i, j, old_i, old_j):
        new_square = self.board[i][j]
        old_square = self.board[old_i][old_j]

        args = (new_square, self.board, self.board_rotation)

        self.squareColorChange(old_i, old_j)

        if old_square.analyseMove(*args):
            old_square.movePiece(new_square)
            return 1

        else:
            return 0

    def sameColorClick(self, i, j, old_i, old_j):
        new_square = self.board[i][j]
        old_square = self.board[old_i][old_j]

        self.squareColorChange(old_i, old_j)

        coord = (i, j)
    
        if new_square == old_square:
            coord = 0

        else:
            self.squareColorChange(i, j)
            
        return coord
        
    def otherColorClick(self, i, j, old_i, old_j):
        new_square = self.board[i][j]
        old_square = self.board[old_i][old_j]

        args = (new_square, self.board, self.board_rotation)

        self.squareColorChange(old_i, old_j)

        if old_square.analyseMove(*args):
            self.capturePiece(old_square, new_square)
            old_square.movePiece(new_square)
            return 1

        else:
            return 0

    def capturePiece(self, old_square, new_square):
        return old_square.capturePiece(new_square, self)