class GameState():

    def __init__(self):
        self.whiteToMove = True  # turno das brancas
        self.clicked = 0  # verifica a peça que foi clicada
        self.moveLog = []
        self.check = False
        self.doubleCheck = False
        self.checkMate = False
        self.whiteKingPosition = (7,4)
        self.blackKingPosition = (0,4)

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