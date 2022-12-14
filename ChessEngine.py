from classes.CastlingRights import CastlingRights
from classes.Piece import King,Rook
from classes.Colors import Color
from classes.Board import Board
from typing import Union, Any

class GameState():

    def __init__(self, rotation: bool) -> None:
        self._whiteToMove = True  # turno das brancas
        self._clicked = 0  # verifica a peça que foi clicada
        self.moveLog: list[Any] = []
        self._checkMate = False
        self._staleMate = False
        if rotation:
            self.whiteKingPosition = (7, 4)
            self.blackKingPosition = (0, 4)
        else:
            self.whiteKingPosition = (0, 4)
            self.blackKingPosition = (7, 4)

        self.currentCastlingRight = CastlingRights(True,True,True,True)

    @property
    def whiteToMove(self) -> bool:
        return self._whiteToMove

    @whiteToMove.setter
    def whiteToMove(self, other: bool) -> None:
        self._whiteToMove = other

    @property
    def clicked(self) -> Any:
        return self._clicked

    @clicked.setter
    def clicked(self, other: Any) -> None:
        self._clicked = other

    @property
    def checkMate(self) -> bool:
        return self._checkMate

    @checkMate.setter
    def checkMate(self, other: bool) -> None:
        self._checkMate = other

    @property
    def staleMate(self) -> bool:
        return self._staleMate

    @staleMate.setter
    def staleMate(self, other: bool) -> None:
        self._staleMate = other

    def shiftChange(self, board: Board) -> None:  # mudança de turno
        if self.whiteToMove == True:
            self.whiteToMove = False
        else:
            self.whiteToMove = True
        self.getAllValidMoves(board)
    
        
    def getAllEnemyPossibleMoves(self, board: Board) -> list[tuple[int, int]]:
        moves = []
        if self.whiteToMove:

            for blackPiece in board.black_pieces:

                if blackPiece.ID == "p":
                    for move in blackPiece.captureList(board, True):
                        moves.append(move)
                else:
                    for move in blackPiece.moveList(board):
                        moves.append(move)
        
        else:

            for whitePiece in board.white_pieces:
                if whitePiece.ID == "p":
                    for move in whitePiece.captureList(board, True):
                        moves.append(move)

                else:
                    for move in whitePiece.moveList(board):
                        moves.append(move)

        return moves
    
    def squareUnderAttack(self, square_i: int, square_j: int, board: Board) -> bool:
        
        # Buscamos pelos movimentos inimigos que atacam o square desejado
        enemyMoves = self.getAllEnemyPossibleMoves(board)

        for move in enemyMoves:

            if move[0] == square_i and move[1] == square_j:
                return True
    
        return False
    
    def inCheck(self,board: Board) -> bool:
        """
            Verifica se o jogador da vez está em xeque
        """
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingPosition[0],self.whiteKingPosition[1],board)

        else:
            return self.squareUnderAttack(self.blackKingPosition[0],self.blackKingPosition[1],board)

    def getAllValidMoves(self, board: Board)-> list[tuple[int, int]]:
        """
            retorna todos os movimentos válidos do jogador da vez
            OBS: se len(allValidMoves) == 0 temos um xequemate ou stalemate
        """
        allValidMoves: list[tuple[int, int]] = []

        if self.whiteToMove:

            for white_piece in board.white_pieces:
                allValidMoves += white_piece.validMoves(self, board)

        else:
            for black_piece in board.black_pieces:
                allValidMoves += black_piece.validMoves(self, board)

        if len(allValidMoves) == 0:

            if self.inCheck(board):
                self.checkMate = True

            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        return allValidMoves

    def getCastleMoves(self,board: Board) -> bool:

        return self.inCheck(board)
    
    def getKingSideCastleMoves(self,board: Board) -> None:
        """"
            Realiza o movimento do rei e da torre no roque a direita
        """
        rotation = board.board_rotation
        if rotation:
            r_coord = 4

        else:
            r_coord = 5

        if self.whiteToMove:

            if self.currentCastlingRight.whiteKingSide:
                row = self.whiteKingPosition[0]
                col2 = self.whiteKingPosition[1] + 2

                whiteKing = board.board[row][self.whiteKingPosition[1]].piece
                whiteRightRook = board.board[row][7].piece

                if whiteKing is not None and whiteRightRook is not None:
                    # Movimento do rei no roque
                    kingCastled = board.addPiece(King,Color.WHITE,row, col2)
                    board.white_pieces.remove(whiteKing)
                    board.white_pieces.append(kingCastled)
                    board.board[row][col2].piece = kingCastled
                    board.board[row][self.whiteKingPosition[1]].piece = None

                    self.whiteKingPosition = (row,col2)

                    # Movimento da torre no roque
                    rookCastled = board.addPiece(Rook,Color.WHITE,row, r_coord)
                    board.white_pieces.remove(whiteRightRook)
                    board.white_pieces.append(rookCastled)
                    board.board[row][r_coord].piece = rookCastled
                    board.board[row][7].piece = None

                    self.currentCastlingRight.whiteKingSide = False
                    self.currentCastlingRight.whiteQueenSide = False
        else:

            if self.currentCastlingRight.blackKingSide:
                row = self.blackKingPosition[0]
                col2 = self.blackKingPosition[1] + 2

                blackKing = board.board[row][self.blackKingPosition[1]].piece
                blackRightRook = board.board[row][7].piece

                if blackKing is not None and blackRightRook is not None:
                    # Movimento do rei no roque
                    kingCastled = board.addPiece(King, Color.BLACK, row, col2)
                    board.black_pieces.remove(blackKing)
                    board.black_pieces.append(kingCastled)
                    board.board[row][col2].piece = kingCastled
                    board.board[row][self.blackKingPosition[1]].piece = None

                    self.blackKingPosition = (row,col2)

                    # Movimento da torre no roque
                    rookCastled = board.addPiece(Rook,Color.BLACK,row, r_coord)
                    board.black_pieces.remove(blackRightRook)
                    board.black_pieces.append(rookCastled)
                    board.board[row][r_coord].piece = rookCastled
                    board.board[row][7].piece = None

                    self.currentCastlingRight.blackKingSide = False
                    self.currentCastlingRight.blackQueenSide = False

    
    def getQueenSideCastleMoves(self,board: Board) -> None:
        """"
            Realiza o movimento do rei e da torre no roque a esquerda
        """

        rotation = board.board_rotation
        if rotation:
            l_coord = 2
        else:
            l_coord = 3

        if self.whiteToMove:

            if self.currentCastlingRight.whiteQueenSide:
        
                row = self.whiteKingPosition[0]
                col2 = self.whiteKingPosition[1] - 2

                whiteKing = board.board[row][self.whiteKingPosition[1]].piece
                whiteLeftRook = board.board[row][0].piece

                if whiteKing is not None and whiteLeftRook is not None:
                    # Movimento do rei no roque
                    kingCastled = board.addPiece(King,Color.WHITE,row, col2)
                    board.white_pieces.remove(whiteKing)
                    board.white_pieces.append(kingCastled)
                    board.board[row][col2].piece = kingCastled
                    board.board[row][self.whiteKingPosition[1]].piece = None

                    self.whiteKingPosition = (row,col2)

                    # Movimento da torre no roque
                    rookCastled = board.addPiece(Rook,Color.WHITE,row, l_coord)
                    board.white_pieces.remove(whiteLeftRook)
                    board.white_pieces.append(rookCastled)
                    board.board[row][l_coord].piece = rookCastled
                    board.board[row][0].piece = None

                    self.currentCastlingRight.whiteKingSide = False
                    self.currentCastlingRight.whiteQueenSide = False
        else:

            if self.currentCastlingRight.blackQueenSide:
                row = self.blackKingPosition[0]
                col2 = self.blackKingPosition[1] - 2

                blackKing = board.board[row][self.blackKingPosition[1]].piece
                blackLeftRook = board.board[row][0].piece

                if blackKing is not None and blackLeftRook is not None:
                    # Movimento do rei no roque
                    kingCastled = board.addPiece(King,Color.BLACK,row, col2)
                    board.black_pieces.remove(blackKing)
                    board.black_pieces.append(kingCastled)
                    board.board[row][col2].piece = kingCastled
                    board.board[row][self.blackKingPosition[1]].piece = None

                    self.blackKingPosition = (row,col2)

                    # Movimento da torre no roque
                    rookCastled = board.addPiece(Rook,Color.BLACK,row, l_coord)
                    board.black_pieces.remove(blackLeftRook)
                    board.black_pieces.append(rookCastled)
                    board.board[row][l_coord].piece = rookCastled
                    board.board[row][0].piece = None

                    self.currentCastlingRight.blackKingSide = False
                    self.currentCastlingRight.blackQueenSide = False
