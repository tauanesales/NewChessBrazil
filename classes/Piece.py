from abc import ABC, abstractmethod
from enum import Enum

class Color(Enum): # uso do enum para as cores
    WHITE = 1
    BLACK = 2

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

    @property
    def color(self):
        return self._color

    @abstractmethod
    def move(self, new_square, old_square):
        pass

    @abstractmethod
    def moveList(self, board):
        pass

    def there_is_piece_between(self, i, j, board): #
        if self.isInRange(i, j):
            if board[i][j].piece == None:
                return 0
            elif board[i][j].returnPieceColor() != self._color:
                return 1
            else:
                return 2
        else:
            return -1

    # método de captura, não precisa verificar a cor, já implantado no move
    def capture(self, new_square):

        if self.move and new_square.piece != None:
            return True

    # caso a peça esteja dentro dos parâmetros, para não usar try para tratar erros
    def isInRange(self, i, j):
        if 0 <= i <= 7 and 0 <= j <= 7:
            return True

class Rook(Piece):
    def __init__(self, image, id, i, j):
        super().__init__(image, id, i, j)

    def move(self, new_square, movelist):  # verifica se na lista de movimentos é possível mover a peça à casa desejada
        for i in movelist:  # movelist = lista de tuplas, logo i = tupla
            (i, j) = i
            if (i, j) == (new_square.i, new_square.j):
                return True

    def moveList(self, board):
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

            if self.there_is_piece_between(i_final, j_final, board) == -1:
                directions += 1
            elif self.there_is_piece_between(i_final, j_final, board) == 0:
                movelist.append((i_final, j_final))
            elif self.there_is_piece_between(i_final, j_final, board) == 1:
                movelist.append((i_final, j_final))
                directions += 1
            else:
                directions += 1

        return movelist


class Knight(Piece):
    def __init__(self, image, id, i, j):
        super().__init__(image, id, i, j)

    def moveList(self, board):  # lista de movimentos
        moveList = []
        possible_indexes = [1, -1, 2, -2]  # lista para iteração
        for i in possible_indexes:
            for j in possible_indexes:
                if abs(i) != abs(j):  # cavalo move 2 casas verticais e 1 horizontal/2 horizontais e 1 vertical
                    i_final = self.i + i
                    j_final = self.j + j
                    if self.isInRange(i_final, j_final):  # verificar se as coords finais estão dentro da matriz
                        if board[i_final][j_final].returnPieceColor() != self._color:  # verificar se a peça é da mesma cor
                            moveList.append((i_final, j_final))  # append de uma tupla
        return moveList

    # verifica se na lista de movimentos é possível mover a peça à casa desejada
    def move(self, new_square, movelist):
        for i in movelist:  # movelist = lista de tuplas, logo i = tupla
            #   (i, j) = i
            if i == (new_square.i, new_square.j):
                return True


class Bishop(Piece):
    def __init__(self, image, id, i, j):
        super().__init__(image, id, i, j)

    def move(self, new_square, movelist):
        for i in movelist:
            (i, j) = i
            if (i, j) == (new_square.i, new_square.j):
                return True

    def moveList(self, board):
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

            if self.there_is_piece_between(i_final, j_final, board) == -1:
                directions += 1

            elif self.there_is_piece_between(i_final, j_final, board) == 0:
                movelist.append((i_final, j_final))

            elif self.there_is_piece_between(i_final, j_final, board) == 1:
                movelist.append((i_final, j_final))
                directions += 1

            else:
                directions += 1

        return movelist

class Queen(Piece):
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
    def __init__(self, image, id, i, j):
        super().__init__(image, id, i, j)

    def moveList(self, board):
        kingMoves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        movelist = []
        for i in range(8):
            i_final = self.i + kingMoves[i][0]
            j_final = self.j + kingMoves[i][1]
            if self.there_is_piece_between(i_final, j_final, board) == -1:
                pass
            if self.there_is_piece_between(i_final, j_final, board) == 0:  # não é uma peça aliada (pode ser peça vazia ou inimiga)
                movelist.append((i_final, j_final))
            elif self.there_is_piece_between(i_final, j_final, board) == 1:
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
        moveList = []
        direction = 0
        if self._color == Color.WHITE:
            if self.already_moved:
                possible_moves = [(1, 0)]
            else:
                possible_moves = [(1, 0), (2, 0)]

            for move in possible_moves:
                if direction == 0:
                    i_final = self.i + move[0]
                    j_final = self.j + move[1]
                    if self.there_is_piece_between(i_final, j_final, board) == -1:
                        pass
                    elif self.there_is_piece_between(i_final, j_final, board) == 0:
                        moveList.append((i_final, j_final))
                    elif self.there_is_piece_between(i_final, j_final, board) == 1:
                        direction = 1
                    else:
                        direction = 1

        else:
            if self.already_moved:
                possible_moves = [(-1, 0)]
            else:
                possible_moves = [(-1, 0), (-2, 0)]

            for move in possible_moves:
                if direction == 0:
                    i_final = self.i + move[0]
                    j_final = self.j + move[1]
                    if self.there_is_piece_between(i_final, j_final, board) == -1:
                        pass
                    elif self.there_is_piece_between(i_final, j_final, board) == 0:
                        moveList.append((i_final, j_final))
                    elif self.there_is_piece_between(i_final, j_final, board) == 1:
                        direction = 1
                    else:
                        direction = 1

        return moveList
