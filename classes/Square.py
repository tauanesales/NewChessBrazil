import pyglet.shapes
from pyglet import graphics
from classes.Colors import Color
from typing import Optional, Any, Callable, Union
from classes.Piece import Rook, Knight, Bishop, Queen, King, Pawn


class Square:
    def __init__(self, square: pyglet.shapes.Rectangle, i: int, j: int, width: int, height: int,
                 piece: Union[Rook, Knight, Bishop, Queen, King, Pawn] = None) -> None:
        self.square = square
        self.i = i
        self.j = j
        self.width = width
        self.height = height
        self.piece = piece  # pode conter peça ou não
        self.status = 0
        self.o_color = self.square.color

    @property
    def color(self) -> tuple[int, int, int]:
        return self.square.color

    @color.setter
    def color(self, other: tuple[int, int, int]) -> None:
        self.square.color = other

    def returnPiece(self) -> Optional[Union[Rook, Knight, Bishop, Queen, King, Pawn, Exception]]:
        if self.piece is None:
            raise Exception('There are no pieces in this square.')
        return self.piece

    def returnPoint(self, x: int, y: int) -> bool:
        return (self.i * self.width) <= y < (self.i + 1) * self.width \
               and (self.j * self.height) <= x < (self.j + 1) * self.height

    def returnCoordinates(self) -> tuple[int, int]:
        return self.i, self.j

    def returnPieceColor(self) -> Optional[Color]:
        if self.piece is not None:
            return self.piece.color
        return None

    def drawPiece(self) -> Optional[Callable[[Any], Any]]:
        if self.piece is not None:
            return self.piece.image.draw()
        return None

    def pieceMoveList(self, gamestate: Any, board: Any) -> Optional[list[tuple[int, int]]]:
        if self.piece is not None:
            return self.piece.validMoves(gamestate, board)
        return None

    def analyseMove(self, new_square: Any, gamestate: Any, board: Any) -> Optional[bool]:
        if self.piece is not None:
            movelist = self.pieceMoveList(gamestate, board)

            if movelist is not None:
                return self.piece.move(new_square, movelist)
        return None

    def changeImageCoord(self, xf: Optional[int] = None, yf: Optional[int] = None) -> None:  # mudar coords da imagem
        if self.piece is not None:
            if xf is None and yf is None:
                self.piece.image.x = self.j * self.width
                self.piece.image.y = self.i * self.height
            else:
                self.piece.image.x = xf
                self.piece.image.y = yf
                self.piece.image.group = graphics.OrderedGroup(1)

    def analyseCapture(self, new_square: Any) -> Optional[bool]:
        if self.piece is not None:
            return self.piece.canCapture(new_square)
        return None
    
    def updateCastlingRights(self, gamestate: Any) -> None:
        if self.piece is not None:
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

    def movePiece(self, new_square: Any, board: Any, gamestate: Any) -> None:
        if self.piece is not None:
            if self.piece.ID == "K" and new_square.j - self.piece.j == 2:
                gamestate.getKingSideCastleMoves(board)

            elif self.piece.ID == "K" and self.piece.j - new_square.j == 2:
                gamestate.getQueenSideCastleMoves(board)
            else:

                self.piece.i = new_square.i
                self.piece.j = new_square.j

                if self.piece.ID == "K" and self.piece.color == Color.WHITE:
                    gamestate.whiteKingPosition = (new_square.i,new_square.j)

                elif self.piece.ID == "K" and self.piece.color == Color.BLACK:
                    gamestate.blackKingPosition = (new_square.i,new_square.j)

                self.updateCastlingRights(gamestate)

                new_square.piece = self.piece
                self.piece = None
                new_square.changeImageCoord()
                new_square.piece.validMoves(gamestate,board)
                self.verifyPawnPromotion(new_square, board)

    def verifyPawnPromotion(self, new_square: Any, board: Any) -> None:
        if new_square.piece.ID == "p":
            new_square.piece.promotePawn(board)

    def capturePiece(self, new_square: Any, board: Any) -> Optional[Callable[[Any, Any], None]]:
        if self.piece is not None:
            return self.piece.capture(new_square, board)
        return None
