from abc import ABC, abstractmethod
from classes.Colors import Color
import pyglet
from time import sleep


class Piece(ABC):
    
    def __init__(self, image, id, i, j):
        self.image = image # desenho da peça
        self.id = id # id da peça
        if self.id[0] == "w":
            self._color = Color.WHITE
        else:
            self._color = Color.BLACK
        self.i = i
        self.j = j

    def __eq__(self, other):
        if other is not None:
            return self.i == other.i and self.j == other.j

    @property
    def color(self):
        return self._color

    @abstractmethod
    def move(self, new_square, old_square):
        pass

    @abstractmethod
    def moveList(self, board):
        pass
    
    def validMoves(self, gamestate, board):
        validMoves = self.moveList(board)
        matrix = board.board

        # Vamos iterar sobre validMoves de tras para a frente retirando os movimentos não válidos
        for i in range(len(validMoves) -1,-1,-1):
            valid = validMoves[i]

            # Agora iremos simular o movimento da peça, se isso permitir que o inimigo coloque o seu rei em xeque sem mover nenhuma peça não é um movimento válido
            temp = matrix[valid[0]][valid[1]].piece

            if matrix[self.i][self.j].piece.ID == "K" and self.color == Color.WHITE:
                gamestate.whiteKingPosition = (valid[0], valid[1])

            elif matrix[self.i][self.j].piece.ID == "K" and self.color == Color.BLACK:
                gamestate.blackKingPosition = (valid[0], valid[1])

            if temp is not None:
                if self.color == Color.WHITE:
                    for piece in board.black_pieces:
                        if piece is matrix[valid[0]][valid[1]].piece:
                            board.black_pieces.remove(piece)

                else:
                    for piece in board.white_pieces:
                        if piece is matrix[valid[0]][valid[1]].piece:
                            board.white_pieces.remove(piece)

            matrix[valid[0]][valid[1]].piece = matrix[self.i][self.j].piece
            matrix[self.i][self.j].piece = None

            # if board.board[validMoves[i][0]][validMoves[i][1]].square.piece != None:


            if gamestate.inCheck(board):
                validMoves.remove(valid)

            matrix[self.i][self.j].piece = matrix[valid[0]][valid[1]].piece
            matrix[valid[0]][valid[1]].piece = temp

            if matrix[self.i][self.j].piece.ID == "K" and self.color == Color.WHITE:
                gamestate.whiteKingPosition = (self.i, self.j)

            elif matrix[self.i][self.j].piece.ID == "K" and self.color == Color.BLACK:
                gamestate.blackKingPosition = (self.i, self.j)

            if temp is not None:
                if self.color == Color.WHITE:
                    board.black_pieces.append(temp)
                else:
                    board.white_pieces.append(temp)

        return validMoves

    def returnPoint(self, x, y, width, height):  # retorna True se for clicado na casa
        return (self.i * width) <= y < (self.i + 1) * width \
               and (self.j * height) <= x < (self.j + 1) * height

    def there_is_piece_between(self, i, j, matrix):
        if self.isInRange(i, j):

            if matrix[i][j].piece is None:
                return 0

            elif matrix[i][j].returnPieceColor() != self.color:
                return 1

            else:
                return 2

        else:
            return -1

    # método de captura, não precisa verificar a cor, já implantado no move
    def canCapture(self, new_square):
        if self.move and new_square.piece is not None:
            return True

    def capture(self, new_square, board):
        if new_square.returnPieceColor() == Color.WHITE:
            for piece in board.white_pieces:
                if new_square.piece == piece:
                    board.white_pieces.remove(piece)

        else:
            for piece in board.black_pieces:
                if new_square.piece == piece:
                    board.black_pieces.remove(piece)

    # caso a peça esteja dentro dos parâmetros, para não usar try para tratar erros
    def isInRange(self, i, j):
        if 0 <= i <= 7 and 0 <= j <= 7:
            return True

class Rook(Piece):
    ID = "R"
    def __init__(self, image, id, i, j):
        super().__init__(image, id, i, j)
        self.already_moved = False

    def move(self, new_square, movelist):  # verifica se na lista de movimentos é possível mover a peça à casa desejada
        for i in movelist:  # movelist = lista de tuplas, logo i = tupla
            (i, j) = i

            if (i, j) == (new_square.i, new_square.j):
                return True

    def moveList(self, board):
        matrix = board.board
        movelist = []
        possible_move = [1, 1, 1, 1]  # [norte, leste, sul, oeste]
        directions = 0

        while directions < 4:

            if directions == 0:
                i_final, j_final = self.i, self.j + possible_move[directions]

            elif directions == 1:
                i_final, j_final = self.i + possible_move[directions], self.j

            elif directions == 2:
                i_final, j_final = self.i, self.j - possible_move[directions]

            else:
                i_final, j_final = self.i - possible_move[directions], self.j

            possible_move[directions] += 1

            if self.there_is_piece_between(i_final, j_final, matrix) == -1:
                directions += 1

            elif self.there_is_piece_between(i_final, j_final, matrix) == 0:
                movelist.append((i_final, j_final))

            elif self.there_is_piece_between(i_final, j_final, matrix) == 1:
                movelist.append((i_final, j_final))
                directions += 1

            else:
                directions += 1

        return movelist


class Knight(Piece):
    
    ID = "N"
    def __init__(self, image, id, i, j):
        super().__init__(image, id, i, j)
    
    def moveList(self, board):  # lista de movimentos
        matrix = board.board
        moveList = []
        possible_indexes = [1, -1, 2, -2]  # lista para iteração

        for i in possible_indexes:

            for j in possible_indexes:

                if abs(i) != abs(j):  # cavalo move 2 casas verticais e 1 horizontal/2 horizontais e 1 vertical
                    i_final = self.i + i
                    j_final = self.j + j

                    if self.there_is_piece_between(i_final, j_final, matrix) in (0, 1):  # verificar se as coords finais estão dentro da matriz
                        moveList.append((i_final, j_final))  # append de uma tupla
        return moveList

    # verifica se na lista de movimentos é possível mover a peça à casa desejada
    def move(self, new_square, movelist):

        for i in movelist:  # movelist = lista de tuplas, logo i = tupla

            if i == (new_square.i, new_square.j):
                return True


class Bishop(Piece):
    ID = "B"
    def __init__(self, image, id, i, j):
        super().__init__(image, id, i, j)

    def move(self, new_square, movelist):
        for i in movelist:
            (i, j) = i

            if (i, j) == (new_square.i, new_square.j):
                return True

    def moveList(self, board):
        matrix = board.board
        movelist = []
        possible_move = [1, 1, 1, 1]  # [1º quadrante, 2º quad, 3º quad, 4º quad]
        directions = 0
        while directions < 4:

            if directions == 0:
                i_final, j_final = self.i + possible_move[directions], \
                                   self.j + possible_move[directions]

            elif directions == 1:
                i_final, j_final = self.i - possible_move[directions], \
                                   self.j + possible_move[directions]

            elif directions == 2:
                i_final, j_final = self.i - possible_move[directions], \
                                   self.j - possible_move[directions]

            else:
                i_final, j_final = self.i + possible_move[directions], \
                                   self.j - possible_move[directions]

            possible_move[directions] += 1

            if self.there_is_piece_between(i_final, j_final, matrix) == -1:
                directions += 1

            elif self.there_is_piece_between(i_final, j_final, matrix) == 0:
                movelist.append((i_final, j_final))

            elif self.there_is_piece_between(i_final, j_final, matrix) == 1:
                movelist.append((i_final, j_final))
                directions += 1

            else:
                directions += 1

        return movelist

class Queen(Piece):
    ID = "Q"
    def __init__(self, image, id, i, j):
        super().__init__(image, id, i, j)

    def move(self, new_square, movelist):
        for i in movelist:
            (i, j) = i
            if (i, j) == (new_square.i, new_square.j):
                return True

    def moveList(self, board):
        movelist = []
        movelist += Rook.moveList(self, board)
        movelist += Bishop.moveList(self, board)
        return movelist

class King(Piece):
    ID = "K"
    def __init__(self, image, id, i, j):
        super().__init__(image, id, i, j)
        self.already_moved = False

    def moveList(self, board):
        matrix = board.board
        kingMoves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        movelist = []

        for i in range(8):
            i_final = self.i + kingMoves[i][0]
            j_final = self.j + kingMoves[i][1]
        

            if self.there_is_piece_between(i_final, j_final, matrix) == -1:
                pass

            elif self.there_is_piece_between(i_final, j_final, matrix) == 0:  # não é uma peça aliada (pode ser peça vazia ou inimiga)
                movelist.append((i_final, j_final))

            elif self.there_is_piece_between(i_final, j_final, matrix) == 1:
                movelist.append((i_final, j_final))

            else:
                pass
        
        return movelist
    

    def verifyCastlePieces(self,board,gamestate,direction):

        canCastle = True

        if direction == "right":
            for col in range(5,7):
                
                if self.there_is_piece_between(self.i,col,board.board) == 1 or self.there_is_piece_between(self.i,col,board.board) == 2 or gamestate.squareUnderAttack(self.i,col,board) :
                    canCastle = False
                
        else:

            for col in range(1,4):
                if self.there_is_piece_between(self.i,col,board.board) == 1 or self.there_is_piece_between(self.i,col,board.board) == 2 or gamestate.squareUnderAttack(self.i,col,board):
                    canCastle = False
        
        return canCastle

    def validMoves(self, gamestate, board):
        castleMoves = []
        
        if self.color == Color.WHITE:

            if gamestate.currentCastlingRight.whiteKingSide and self.verifyCastlePieces(board,gamestate,direction="right"):
                castleMoves += [(self.i,2 + self.j)]
                
            if gamestate.currentCastlingRight.whiteQueenSide and self.verifyCastlePieces(board,gamestate,direction="left"):
                castleMoves += [(self.i, self.j - 2)]
   
        else:
            if gamestate.currentCastlingRight.blackKingSide and self.verifyCastlePieces(board, gamestate,direction = "right"):
                castleMoves += [(self.i, self.j + 2)]

            if gamestate.currentCastlingRight.blackQueenSide and self.verifyCastlePieces(board, gamestate,direction = "left"):
                castleMoves += [(self.i, self.j - 2)]
            
            
        return super().validMoves(gamestate,board) + castleMoves

    def move(self, new_square, movelist):
        for i in movelist:
            (i, j) = i
            if (i, j) == (new_square.i, new_square.j):
                return True


class Pawn(Piece):
    ID = "p"
    def __init__(self, image, id, i, j):
        super().__init__(image, id, i, j)
        self.already_moved = False

    def move(self, new_square, moveList):
        for move in moveList:
            if move == (new_square.i, new_square.j):

                if self.already_moved == False:
                    self.already_moved = True

                return True

    def moveList(self, board):
        rotation = board.board_rotation
        matrix = board.board
        moveList = []
        direction = 0

        if self.color == Color.WHITE:

            if self.already_moved:
                possible_moves = [(1, 0)]

            else:
                possible_moves = [(1, 0), (2, 0)]

        else:

            if self.already_moved:
                possible_moves = [(-1, 0)]

            else:
                possible_moves = [(-1, 0), (-2, 0)]

        if rotation:
            possible_moves = [(-1*i[0], 0) for i in possible_moves]

        for move in possible_moves:
            if direction == 0:
                i_final = self.i + move[0]
                j_final = self.j + move[1]

                if self.there_is_piece_between(i_final, j_final, matrix) == 0:
                    moveList.append((i_final, j_final))

                elif self.there_is_piece_between(i_final, j_final, matrix) == 1:
                    direction = 1

                else:
                    direction = 1

        moveList += self.captureList(board)

        return moveList

    def captureList(self, board):
        moveList = []
        matrix = board.board
        rotation = board.board_rotation

        if self.color == Color.WHITE:
            capture_moves = [(1, 1), (1, -1)]

        else:
            capture_moves = [(-1, 1), (-1, -1)]

        if rotation:
            capture_moves = [(-1*i[0], i[1]) for i in capture_moves]

        for move in capture_moves:
            i_final = self.i + move[0]
            j_final = self.j + move[1]

            if self.there_is_piece_between(i_final, j_final, matrix) == 1:
                moveList.append((i_final, j_final))

        return moveList

    def checkPromotion(self, board):
        
        
        if self.color == Color.WHITE:
            if board.board_rotation:
                
                if self.i == 0:
                    return True
                else:
                    return False
            else:

                if self.i == 7:
                    return True
                else:
                    return False
        else:

            if board.board_rotation:

                if self.i == 7:
                    return True
                else:
                    return False
            else:
                if self.i == 0:
                    return True
                else:
                    return False

    def promotePawn(self,board):

        if self.checkPromotion(board):
            
            chosen = self.showPromotionMenu(board)

            if self.color == Color.WHITE:
                
                
                pawnPromoted = board.addPiece(chosen ,Color.WHITE,self.i,self.j)

                for piece in board.white_pieces:
                    if piece == self:
                        board.white_pieces.remove(piece)
                    
                board.white_pieces.append(pawnPromoted)
                board.board[self.i][self.j].piece = pawnPromoted

            else:
                
                pawnPromoted = board.addPiece(chosen, Color.BLACK,self.i,self.j)

                for piece in board.black_pieces:
                    if piece == self:
                        board.black_pieces.remove(piece)
                    
                board.black_pieces.append(pawnPromoted)
                board.board[self.i][self.j].piece = pawnPromoted

    def showPromotionMenu(self,board):
        ids =["B","N","Q","R"]
        images = {}
        chosen = None
        i = 0
        distance = 64
        height = 64
        window = pyglet.window.Window(width = distance*4, height = height)
        if self.color == Color.WHITE and self.checkPromotion(board):

            for id in ids:
                piece = "w" + id
                images[piece] = pyglet.image.load("public/" + piece + ".png")
                
                images[piece] = pyglet.sprite.Sprite(images[piece], x = i * distance, y = 0)

                i += 1
        elif self.color == Color.BLACK and self.checkPromotion(board):
            for id in ids:
                piece = "b" + id
                images[piece] = pyglet.image.load("public/" + piece + ".png")

                images[piece] = pyglet.sprite.Sprite(images[piece], x = i * distance, y = 0)

                i += 1

        @window.event
        def on_draw():
            window.clear()

            for piece in images:
                images[piece].draw()

        @window.event
        def on_mouse_release(x, y, buttons, modifiers):
            if 0 <= x <= distance*1:
                chosen = Bishop

            elif distance*1 < x <= distance*2:
                chosen = Knight
            
            elif distance*2 < x <= distance*3:
                chosen = Queen
            
            else:
                chosen = Rook

            window.close()

        return chosen
            

        
