import pyglet
from classes.Square import Square
from classes.Piece import *
from classes.Colors import *
from random import choice
from typing import Any, Union, Optional, Type


class Board:

    def __init__(self, width: int, height: int) -> None:
        self.board: list[list[Square]] = []
        self.white_pieces: list[Union[Rook, Knight, Bishop, Queen, King, Pawn]] = []
        self.black_pieces: list[Union[Rook, Knight, Bishop, Queen, King, Pawn]] = []
        self.width = width
        self.height = height
        self.dimension = 8  # tabuleiro 8x8
        self.images: dict[str, Any] = {}  # dict de sprites das peças
        self.batch = pyglet.graphics.Batch()  # batch para renderizar com mais eficiência
        self.sprites: list[Any] = []  # lista dos shapes da casa para renderização (batch)
        self.board_rotation: bool = choice([False, True])

        self.loadImages()
        self.createPieces()

    @property
    def square_size(self) -> int:
        return self.height // self.dimension

    def loadImages(self) -> None:
        pieces = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR", "bp",
                  "wp", "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]

        for piece in pieces:
            self.images[piece] = pyglet.image.load("public/" + piece + ".png")

    def createBoard(self) -> None:  # criação do tabuleiro
        colors = [sColor.WHITE.value, sColor.GRAY.value]  # cor branca e cinza, alternância

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


    def addPiece(self, piece: Union[Type[Rook], Type[Knight], Type[Bishop], Type[Queen],
                                    Type[King], Type[Pawn]], color: Any, i: int, j: int) -> Any:
        id = color.value + piece.ID
        sprite = pyglet.sprite.Sprite(self.images[id], x = self.square_size*j,
                                    y = self.square_size*i)

        
        return piece(sprite, id, i, j)

    def createPieces(self) -> None:  # inserção das peças, contidas na casa

        self.createBoard()
        pieces = []

        if self.board_rotation:
            i = 7
            king_pos = 3
            queen_pos = 4
        else:
            i = 0
            king_pos = 4
            queen_pos = 3

        rook_w1 = self.addPiece(Rook, Color.WHITE, i, 0)
        rook_w2 = self.addPiece(Rook, Color.WHITE, i, 7)

        knight_w1 = self.addPiece(Knight ,Color.WHITE, i, 1)
        knight_w2 = self.addPiece(Knight, Color.WHITE, i, 6)

        bishop_w1 = self.addPiece(Bishop, Color.WHITE, i, 2)
        bishop_w2 = self.addPiece(Bishop, Color.WHITE, i, 5)

        queen_w = self.addPiece(Queen, Color.WHITE, i, queen_pos)

        king_w = self.addPiece(King, Color.WHITE, i, king_pos)

        column = [rook_w1, knight_w1, bishop_w1, queen_w, king_w, bishop_w2, knight_w2, rook_w2]
        self.white_pieces += column

        if self.board_rotation:
            i = 6

        else:
            i = 1

        for j in range(8):
            pawn_w = self.addPiece(Pawn, Color.WHITE, i, j)
            self.white_pieces.append(pawn_w)

        if self.board_rotation:
            i = 1

        else:
            i = 6

        # Black
        for j in range(8):
            pawn_b = self.addPiece(Pawn, Color.BLACK, i, j)
            self.black_pieces.append(pawn_b)

        if self.board_rotation:
            i = 0
            king_pos = 3
            queen_pos = 4

        else:
            i = 7
            king_pos = 4
            queen_pos = 3

        rook_b1 = self.addPiece(Rook, Color.BLACK, i, 0)
        rook_b2 = self.addPiece(Rook, Color.BLACK, i, 7)

        knight_b1 = self.addPiece(Knight ,Color.BLACK, i, 1)
        knight_b2 = self.addPiece(Knight, Color.BLACK, i, 6)


        bishop_b1 = self.addPiece(Bishop, Color.BLACK, i, 2)
        bishop_b2 = self.addPiece(Bishop, Color.BLACK, i, 5)

        queen_b = self.addPiece(Queen, Color.BLACK, i, queen_pos)

        king_b = self.addPiece(King, Color.BLACK, i, king_pos)

        column = [rook_b1, knight_b1, bishop_b1, queen_b, king_b, bishop_b2, knight_b2, rook_b2]
        self.black_pieces += column

        pieces += self.white_pieces
        pieces += self.black_pieces

        for piece in pieces:
            i, j = piece.i, piece.j
            self.board[i][j].piece = piece

    def squareColorChange(self, i: int, j: int, gamestate: Any) -> None: 
        actual_square = self.board[i][j]
        moveList = actual_square.pieceMoveList(gamestate, self)

        if actual_square.status == 0:  # caso não esteja clicado
            actual_square.status = 1
            actual_square.color = sColor.CLICKED.value

            if moveList is not None:
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
            self.revertBoardColor()

    def revertBoardColor(self) -> None:
        for line in self.board:
            for square in line:

                if square.color != square.o_color:
                    square.color = square.o_color

    def pieceClick(self, x: int, y: int, gamestate: Any) -> Union[tuple[int, int], int]:
        shift = gamestate.whiteToMove

        if shift:
            for piece in self.white_pieces:
                i, j = piece.i, piece.j
                if piece.returnPoint(x, y, self.square_size, self.square_size):
                    self.squareColorChange(i, j, gamestate)
                    return (i, j)

        else:
            for piece in self.black_pieces:
                i, j = piece.i, piece.j
                if piece.returnPoint(x, y, self.square_size, self.square_size):
                    self.squareColorChange(i, j, gamestate)
                    return (i, j)

        return 0

    def squareClick(self, x: int, y: int) -> tuple[Optional[int], Optional[int]]:
        i = j = None

        for line in self.board:
            for square in line:

                if square.returnPoint(x, y):
                    i, j = square.returnCoordinates()

        if i is None and j is None:
            raise TypeError('No squares were clicked.')

        else:
            return i, j

    def isSameColor(self, i: int, j: int, old_i: int, old_j: int) -> Optional[bool]:
        new_square = self.board[i][j]
        old_square = self.board[old_i][old_j]

        if new_square.returnPieceColor() is None:
            return None

        elif new_square.returnPieceColor() == old_square.returnPieceColor():
            return True

        else:
            return False

    def dragSquareSwitch(self, coord: Union[int, tuple[int, int]], gamestate: Any) -> None:
        clicked = gamestate.clicked

        if type(coord) == type(clicked) and type(coord) == tuple:
            (i, j) = coord
            (other_i, other_j) = clicked
            self.squareColorChange(i, j, gamestate)

            if coord != clicked:
                self.squareColorChange(other_i, other_j, gamestate)
                self.squareColorChange(i, j, gamestate)

    def noColorClick(self, i: int, j: int, old_i: int, old_j: int, gamestate: Any) -> int:
        new_square = self.board[i][j]
        old_square = self.board[old_i][old_j]

        args = (new_square, gamestate, self)

        self.squareColorChange(old_i, old_j, gamestate)

        if old_square.analyseMove(*args):
            old_square.movePiece(new_square, self, gamestate)

            return 1

        else:
            return 0

    def samePieceClick(self, i: int, j: int, drag: int, gamestate: Any) -> Any:
        coord: Union[int, tuple[int, int]] = 0

        if drag == 0:
            coord = 0

        else:
            self.squareColorChange(i, j, gamestate)
            coord = (i, j)

        return coord

    def sameColorClick(self, i: int, j: int, old_i: int, old_j: int, drag: int, gamestate: Any) -> Any:
        new_square = self.board[i][j]
        old_square = self.board[old_i][old_j]

        self.squareColorChange(old_i, old_j, gamestate)

        coord = (i, j)

        if new_square == old_square:
            coord = self.samePieceClick(i, j, drag, gamestate)

        else:
            self.squareColorChange(i, j, gamestate)

        return coord

    def otherColorClick(self, i: int, j: int, old_i: int, old_j: int, gamestate: Any) -> int:

        new_square = self.board[i][j]
        old_square = self.board[old_i][old_j]

        args = (new_square, gamestate, self)

        self.squareColorChange(old_i, old_j, gamestate)

        if old_square.analyseMove(*args):
            self.capturePiece(old_square, new_square)
            old_square.movePiece(new_square, self, gamestate)
            return 1

        else:
            return 0

    def capturePiece(self, old_square, new_square):
        return old_square.capturePiece(new_square, self)

    def returnSquareXY(self, i, j):
        square = self.board[i][j]
        return square.height * square.i, square.width * square.j
