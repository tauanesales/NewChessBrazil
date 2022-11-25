from classes.CastlingRights import CastlingRights
from classes.Piece import King,Rook
from classes.Colors import Color

class GameState():

    def __init__(self, rotation):
        self.whiteToMove = True  # turno das brancas
        self.clicked = 0  # verifica a peça que foi clicada
        self.moveLog = []
        self.checkMate = False
        self.staleMate = False
        if rotation:
            self.whiteKingPosition = (7, 4)
            self.blackKingPosition = (0, 4)
        else:
            self.whiteKingPosition = (0, 4)
            self.blackKingPosition = (7, 4)

        self.currentCastlingRight = CastlingRights(True,True,True,True)

        
    def shiftChange(self):  # mudança de turno
        if self.whiteToMove == True:
            self.whiteToMove = False
        else:
            self.whiteToMove = True

    def getAllEnemyPossibleMoves(self, board):
        moves = []
        if self.whiteToMove:

            for blackPiece in board.black_pieces:

                if blackPiece.ID == "p":
                    for move in blackPiece.captureList(board):
                        moves.append(move)
                else:
                    for move in blackPiece.moveList(board):
                        moves.append(move)
        
        else:

            for whitePiece in board.white_pieces:
                if whitePiece.ID == "p":
                    for move in whitePiece.captureList(board):
                        moves.append(move)

                else:
                    for move in whitePiece.moveList(board):
                        moves.append(move)

        return moves
    
    def squareUnderAttack(self,square_i,square_j,board):
        
        # Buscamos pelos movimentos inimigos que atacam o square desejado
        enemyMoves = self.getAllEnemyPossibleMoves(board)

        for move in enemyMoves:

            if move[0] == square_i and move[1] == square_j:
                return True
    
        return False
    
    def inCheck(self,board):
        """
            Verifica se o jogador da vez está em xeque
        """
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingPosition[0],self.whiteKingPosition[1],board)

        else:
            return self.squareUnderAttack(self.blackKingPosition[0],self.blackKingPosition[1],board)

    def getAllValidMoves(self, board):
        """
            retorna todos os movimentos válidos do jogador da rodada
            OBS: se len(allValidMoves) == 0 temos um xequemate ou stalemate
        """
        allValidMoves = []

        if self.whiteToMove:

            for white_piece in board.white_pieces:
                allValidMoves.append(white_piece.validMoves())

        else:
            for black_piece in board.black_pieces:
                allValidMoves.append(black_piece.validMoves())

        if len(allValidMoves) == 0:

            if self.inCheck(board):
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        return allValidMoves

    def getCastleMoves(self,board):

        return self.inCheck(board)
    
    def getKingSideCastleMoves(self,board):
        """"
            Realiza o movimento do rei e da torre no roque a direita
        """

        if self.whiteToMove:

            if self.currentCastlingRight.whiteKingSide:
                row = self.whiteKingPosition[0]
                col1 = self.whiteKingPosition[1] + 1
                col2 = self.whiteKingPosition[1] + 2

                whiteKing = board.board[row][self.whiteKingPosition[1]].piece
                whiteRightRook = board.boar[row][7].piece

                if self.squareUnderAttack(row,col1, board) == False and  self.squareUnderAttack(row,col2, board) == False and board[row][col1].piece == None and board[row][col2].piece == None:
                    
                    # Movimento do rei no roque
                    kingCastled = board.addPiece(King,Color.WHITE,row, col2)
                    board.white_pieces.remove(whiteKing)
                    board.white_pieces.append(kingCastled)
                    board.board[row][col2].piece = kingCastled

                    # Movimento da torre no roque    
                    rookCastled = board.addPiece(Rook,Color.WHITE,row, 5)
                    board.white_pieces.remove(whiteRightRook)
                    board.white_pieces.append(rookCastled)
                    board.board[row][5].piece = rookCastled
        
        else:

            if self.currentCastlingRight.blackKingSide:
                row = self.blackKingPosition[0]
                col1 = self.blackKingPosition[1] + 1
                col2 = self.blackKingPosition[1] + 2

                blackKing = board.board[row][self.blackKingPosition[1]].piece
                blackRightRook = board.boar[row][7].piece

                if self.squareUnderAttack(row,col1, board) == False and  self.squareUnderAttack(row,col2, board) == False and board[row][col1].piece == None and board[row][col2].piece == None:
                    # Movimento do rei no roque
                    kingCastled = board.addPiece(King,Color.BLACK,row, col2)
                    board.black_pieces.remove(blackKing)
                    board.black_pieces.append(kingCastled)
                    board.board[row][col2].piece = kingCastled

                    # Movimento da torre no roque    
                    rookCastled = board.addPiece(Rook,Color.BLACK,row, 5)
                    board.black_pieces.remove(blackRightRook)
                    board.black_pieces.append(rookCastled)
                    board.board[row][5].piece = rookCastled
                    

    
    def getQueenSideCastleMoves(self,board):
        """"
            Realiza o movimento do rei e da torre no roque a esquerda
        """

        if self.whiteToMove:

            if self.currentCastlingRight.whiteQueenSide:
        
                row = self.whiteKingPosition[0]
                col1 = self.whiteKingPosition[1] - 1
                col2 = self.whiteKingPosition[1] - 2

                whiteKing = board.board[row][self.whiteKingPosition[1]].piece
                whiteLeftRook = board.boar[row][0].piece

                if self.squareUnderAttack(row,col1, board) == False and  self.squareUnderAttack(row,col2, board) == False and board[row][col1].piece == None and board[row][col2].piece == None:
                    
                    # Movimento do rei no roque
                    kingCastled = board.addPiece(King,Color.WHITE,row, col2)
                    board.white_pieces.remove(whiteKing)
                    board.white_pieces.append(kingCastled)
                    board.board[row][col2].piece = kingCastled

                    # Movimento da torre no roque    
                    rookCastled = board.addPiece(Rook,Color.WHITE,row, 3)
                    board.white_pieces.remove(whiteLeftRook)
                    board.white_pieces.append(rookCastled)
                    board.board[row][3].piece = rookCastled
                    
                        
        
        else:

            if self.currentCastlingRight.blackQueenSide:
                row = self.blackKingPosition[0]
                col1 = self.blackKingPosition[1] - 1
                col2 = self.blackKingPosition[1] - 2

                blackKing = board.board[row][self.blackKingPosition[1]].piece
                blackLeftRook = board.boar[row][0].piece

                if self.squareUnderAttack(row,col1, board) == False and  self.squareUnderAttack(row,col2, board) == False and board[row][col1].piece == None and board[row][col2].piece == None:
                    
                    # Movimento do rei no roque
                    kingCastled = board.addPiece(King,Color.BLACK,row, col2)
                    board.black_pieces.remove(blackKing)
                    board.black_pieces.append(kingCastled)
                    board.board[row][col2].piece = kingCastled

                    # Movimento da torre no roque    
                    rookCastled = board.addPiece(Rook,Color.BLACK,row, 3)
                    board.black_pieces.remove(blackLeftRook)
                    board.black_pieces.append(rookCastled)
                    board.board[row][3].piece = rookCastled
    

            