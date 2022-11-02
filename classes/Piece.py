from abc import ABC, abstractmethod
from enum import Enum
from pickle import FALSE

class Color(Enum): # uso do enum para as cores
    WHITE = 1
    BLACK = 2

class Piece(ABC):
    def __init__(self, image, id, width, height, x, y):
        self.image = image # desenho da peça
        self.id = id # id da peça
        self.width = width # largura da peça
        self.height = height # altura da peça
        if self.id[0] == "w":
            self._color = Color.WHITE
        else:
            self._color = Color.BLACK
        self.x = x
        self.y = y

    @property
    def color(self):
        return self._color

    @abstractmethod
    def move(self, new_square, old_square):
        pass

    @abstractmethod
    def moveList(self, board):
        pass

    def there_is_piece_between(self, xf, yf, board):
        if self.isInRange(xf, yf):
            if board[xf + yf * 8].piece == None:
                return 0
            elif board[xf + yf * 8].returnPieceColor() != self._color:
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
    def isInRange(self, x, y):
        if 0 <= x <= 7 and 0 <= y <= 7:
            return True


class Rook(Piece):
    def __init__(self, image, id, width, height, x, y):
        super().__init__(image, id, width, height, x, y)

    # verifica se na lista de movimentos é possível mover a peça à casa desejada
    def move(self, new_square, movelist):
        for i in movelist:  # movelist = lista de tuplas, logo i = tupla
            (x, y) = i
            if (x, y) == (new_square.x, new_square.y):
                return True

    def moveList(self, board):
        movelist = []
        possible_move = [1, 1, 1, 1]  # [norte, leste, sul, oeste]
        directions = 0
        while directions < 4:
            if directions == 0:
                xf, yf = self.x, self.y + possible_move[directions]

            elif directions == 1:
                xf, yf = self.x + possible_move[directions], self.y

            elif directions == 2:
                xf, yf = self.x, self.y - possible_move[directions]

            else:
                xf, yf = self.x - possible_move[directions], self.y

            possible_move[directions] += 1

            if self.there_is_piece_between(xf, yf, board) == -1:
                directions += 1
            elif self.there_is_piece_between(xf, yf, board) == 0:
                movelist.append((xf, yf))
            elif self.there_is_piece_between(xf, yf, board) == 1:
                movelist.append((xf, yf))
                directions += 1
            else:
                directions += 1

        return movelist


class Knight(Piece):
    def __init__(self, image, id, width, height, x, y):
        super().__init__(image, id, width, height, x, y)

    def moveList(self, board):  # lista de movimentos
        moveList = []
        possible_indexes = [1, -1, 2, -2]  # lista para iteração
        for i in possible_indexes:
            for j in possible_indexes:
                # cavalo move 2 casas verticais e 1 horizontal/2 horizontais e 1 vertical
                if abs(i) != abs(j):
                    xf = self.x + i
                    yf = self.y + j
                    # verificar se as coords finais estão dentro da matriz
                    if self.isInRange(xf, yf):
                        # verificar se a peça é da mesma cor
                        if board[xf+yf*8].returnPieceColor() != self._color:
                            moveList.append((xf, yf))  # append de uma tupla
        return moveList

    # verifica se na lista de movimentos é possível mover a peça à casa desejada
    def move(self, new_square, movelist):
        for i in movelist:  # movelist = lista de tuplas, logo i = tupla
            (x, y) = i
            if (x, y) == (new_square.x, new_square.y):
                return True


class Bishop(Piece):
    def __init__(self, image, id, width, height, x, y):
        super().__init__(image, id, width, height, x, y)

    def move(self, new_square, movelist):
        for i in movelist:
            (x, y) = i
            if (x, y) == (new_square.x, new_square.y):
                return True

    def moveList(self, board):
        movelist = []
        # [1º quadrante, 2º quad, 3º quad, 4º quad]
        possible_move = [1, 1, 1, 1]
        directions = 0
        while directions < 4:
            if directions == 0:
                xf, yf = self.x + \
                    possible_move[directions], self.y + \
                    possible_move[directions]

            elif directions == 1:
                xf, yf = self.x - \
                    possible_move[directions], self.y + \
                    possible_move[directions]

            elif directions == 2:
                xf, yf = self.x - \
                    possible_move[directions], self.y - \
                    possible_move[directions]

            else:
                xf, yf = self.x + \
                    possible_move[directions], self.y - \
                    possible_move[directions]

            possible_move[directions] += 1

            if self.there_is_piece_between(xf, yf, board) == -1:
                directions += 1

            elif self.there_is_piece_between(xf, yf, board) == 0:
                movelist.append((xf, yf))

            elif self.there_is_piece_between(xf, yf, board) == 1:
                movelist.append((xf, yf))
                directions += 1

            else:
                directions += 1

        return movelist


class Queen(Piece):
    def __init__(self, image, id, width, height, x, y):
        super().__init__(image, id, width, height, x, y)

    def move(self, new_square, movelist):
        for i in movelist:
            (x, y) = i
            if (x, y) == (new_square.x, new_square.y):
                return True

    def moveList(self, board):
        movelist = []
        movelist += Rook.moveList(self, board)
        movelist += Bishop.moveList(self, board)
        return movelist


class King(Piece):
    def __init__(self, image, id, width, height, x, y):
        super().__init__(image, id, width, height, x, y)

    def moveList(self, board):
        possible_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                          (0, 1), (1, -1), (1, 0), (1, 1)]
        movelist = []
        for i in range(8):
            xf = self.x + possible_moves[i][0]
            yf = self.y + possible_moves[i][1]
            if self.there_is_piece_between(xf, yf, board) == -1:
                pass
            # não é uma peça aliada (pode ser peça vazia ou inimiga)
            if self.there_is_piece_between(xf, yf, board) == 0:
                movelist.append((xf, yf))
            elif self.there_is_piece_between(xf, yf, board) == 1:
                movelist.append((xf, yf))
            else:
                pass
        return movelist

    def move(self, new_square, movelist):
        for i in movelist:
            (x, y) = i
            if (x, y) == (new_square.x, new_square.y):
                return True


class Pawn(Piece):
    def __init__(self, image, id, width, height, x, y):
        super().__init__(image, id, width, height, x, y)
        self.already_moved = False

    def move(self, new_square, moveList):

        for move in moveList:

            if move == (new_square.x, new_square.y):
                if self.already_moved == False:
                    self.already_moved = True
                return True

    def moveList(self, board):
        moveList = []

        if self._color == Color.WHITE:
            if self.already_moved:
                possible_moves = [(0, 1)]
            else:
                possible_moves = [(0, 1), (0, 2)]

            for move in possible_moves:
                xf = self.x + move[0]
                yf = self.y + move[1]

                if self.there_is_piece_between(xf, yf, board) == -1:
                    pass
                elif self.there_is_piece_between(xf, yf, board) == 0:
                    moveList.append((xf, yf))
                elif self.there_is_piece_between(xf, yf, board) == 1:
                    pass
                else:
                    pass
        else:
            if self.already_moved:
                possible_moves = [(0, -1)]
            else:
                possible_moves = [(0, -1), (0, -2)]

            for move in possible_moves:
                xf = self.x + move[0]
                yf = self.y + move[1]

                if self.there_is_piece_between(xf, yf, board) == -1:
                    pass
                elif self.there_is_piece_between(xf, yf, board) == 0:
                    moveList.append((xf, yf))
                elif self.there_is_piece_between(xf, yf, board) == 1:
                    pass
                else:
                    pass
        return moveList