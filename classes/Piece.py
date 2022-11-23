from abc import ABC, abstractmethod
from classes.Colors import Color


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
    def moveList(self, board, rotation):
        pass
    
    def validMoves(self,gamestate,board):
        validMoves = self.moveList(board,board.board_rotation)

        # Vamos iterar sobre validMoves de tras para a frente retirando os movimentos não válidos
        for i in range(len(validMoves) -1,-1,-1):
            
            # Agora iremos simular o movimento da peça, se isso permitir que o inimigo coloque o seu rei em xeque sem mover nenhuma peça não é um movimento válido

            old_i = self.i
            old_j = self.j

            self.i = validMoves[i][0]
            self.j = validMoves[i][1]

            if gamestate.inCheck(board):
                validMoves.remove(validMoves[i])

            self.i = old_i
            self.j = old_j
        return validMoves

    def isCheck(self, board, gamestate):
        # possible_moves = self.moveList(board.board, board.board_rotation)
        matrix = board.board
        rotation = board.board_rotation
        counter = 0
        enemy_king = None
        if gamestate.whiteToMove:
            
            for white_piece in board.white_pieces:
               
                for move in white_piece.moveList(board, rotation):
                    i,j = move

                    piece_in_square = matrix[i][j].piece
                    if piece_in_square is not None:
                        if piece_in_square.ID == King.ID and self.color != piece_in_square.color:
                            check = True
                            counter += 1


                            enemy_king = piece_in_square
                            print("check")
                            # Se a peça no quadrado for o rei alteramos o atributo para representar q ele estar sendo atacado
                            

        else:
             for black_piece in board.black_pieces:
               
                for move in black_piece.moveList(board, rotation):
                    i, j = move
                    piece_in_square = matrix[i][j].piece
                    if piece_in_square is not None:
                        if piece_in_square.ID == King.ID and self.color != piece_in_square.color:
                            check = True
                            counter += 1
                            
                            enemy_king = piece_in_square
                            print("check")
                            # Se a peça no quadrado for o rei alteramos o atributo para representar q ele estar sendo atacado           
        
        if counter == 0:
            gamestate.check = False
            gamestate.doubleCheck = False

        elif counter == 1:

            enemy_king.check = True
            enemy_king.doubleCheck = False

            gamestate.check = True
            gamestate.doublecheck = False

        elif counter == 2:

            enemy_king.check = False
            enemy_king.doubleCheck = True

            gamestate.check = False
            gamestate.doubleCheck = True
            
        else:
            
            enemy_king.check = False
            enemy_king.doubleCheck = False

            gamestate.check = False
            gamestate.doubleCheck = False
             


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

    def move(self, new_square, movelist):  # verifica se na lista de movimentos é possível mover a peça à casa desejada
        for i in movelist:  # movelist = lista de tuplas, logo i = tupla
            (i, j) = i

            if (i, j) == (new_square.i, new_square.j):
                return True

    def moveList(self, board, rotation):
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
    
    def moveList(self, board, rotation):  # lista de movimentos
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

    def moveList(self, board, rotation):
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

    def moveList(self, board, rotation):
        movelist = []
        movelist += Rook.moveList(self, board, rotation)
        movelist += Bishop.moveList(self, board, rotation)
        return movelist

class King(Piece):
    ID = "K"
    def __init__(self, image, id, i, j):
        super().__init__(image, id, i, j)
        self.check = False
        self.doubleCheck = False

    def moveList(self, board, rotation):
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

    def moveList(self, board, rotation):
        matrix = board.board
        moveList = []
        direction = 0

        if self.color == Color.WHITE:

            capture_moves = [(1, 1), (1, -1)]

            if self.already_moved:
                possible_moves = [(1, 0)]

            else:
                possible_moves = [(1, 0), (2, 0)]

        else:

            capture_moves = [(-1, 1), (-1, -1)]

            if self.already_moved:
                possible_moves = [(-1, 0)]

            else:
                possible_moves = [(-1, 0), (-2, 0)]

        if rotation:
            possible_moves = [(-1*i[0], 0) for i in possible_moves]
            capture_moves = [(-1*i[0], i[1]) for i in capture_moves]

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

        for move in capture_moves:
            i_final = self.i + move[0]
            j_final = self.j + move[1]

            if self.there_is_piece_between(i_final, j_final, matrix) == 1:
                moveList.append((i_final, j_final))

        return moveList