class GameState():

    def __init__(self):
        self.whiteToMove = True  # turno das brancas
        self.clicked = 0  # verifica a peça que foi clicada
        self.moveLog = []
        self.whiteKingPosition = (7,4)
        self.blackKingPosition = (0,4)
        self.checkMate = False # quando o rei não possui movimentos válidos e está em xeque
        self.staleMate = False # quanod não há movimentos válidos e o rei não está em xeque

    def shiftChange(self):  # mudança de turno
        if self.whiteToMove == True:
            self.whiteToMove = False
        else:
            self.whiteToMove = True


    def getAllEnemyPossibleMoves(self, board):
        moves = []
        if self.whiteToMove:

            for blackPiece in board.black_pieces:

                for move in blackPiece.moveList(board,board.board_rotation):

                    moves.append(move)
        
        else:

            for whitePiece in board.white_pieces:

                for move in whitePiece.moveList(board,board.board_rotation):

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

    def getAllValidMoves(self,board):
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