from abc import ABC, abstractmethod
from enum import Enum


class Color(Enum):  # uso do enum para as cores
    WHITE = 1
    BLACK = 2


class Piece(ABC):
    def __init__(self, image, id, width, height, x, y):
        self.image = image
        self.id = id
        self.width = width
        self.height = height
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

    def move(self, new_square, movelist):  # verifica se na lista de movimentos é possível mover a peça à casa desejada
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

<<<<<<< HEAD
    def moveList(self, board):  # lista de movimentos
        moveList = []
        possible_indexes = [1, -1, 2, -2]  # lista para iteração
        for i in possible_indexes:
            for j in possible_indexes:
                if abs(i) != abs(j):  # cavalo move 2 casas verticais e 1 horizontal/2 horizontais e 1 vertical
                    xf = self.x + i
                    yf = self.y + j
                    if self.isInRange(xf, yf):  # verificar se as coords finais estão dentro da matriz
                        if board[xf + yf * 8].returnPieceColor() != self._color:  # verificar se a peça é da mesma cor
                            moveList.append((xf, yf))  # append de uma tupla
        return moveList

    # verifica se na lista de movimentos é possível mover a peça à casa desejada
    def move(self, new_square, movelist):
        for i in movelist:  # movelist = lista de tuplas, logo i = tupla
            #   (x, y) = i
            if i == (new_square.x, new_square.y):
                return True
=======
  def moveList(self, board): # lista de movimentos
    moveList = []
    possible_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)] # melhorar o entendimento
    for move in possible_moves:
      (xf, yf) = (self.x + move[0], self.y + move[1])
      if self.isInRange(xf, yf): # verificar se as coords finais estão dentro da matriz
        if board[xf+yf*8].returnPieceColor() != self._color: # verificar se a peça é da mesma cor
          moveList.append((xf, yf)) # append de uma tupla
    return moveList
>>>>>>> 79beea113d86ba652c12178c62566fe510837e9d


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
        possible_move = [1, 1, 1, 1]  # [1º quadrante, 2º quad, 3º quad, 4º quad]
        directions = 0
        while directions < 4:
            if directions == 0:
                xf, yf = self.x + possible_move[directions], self.y + possible_move[directions]

            elif directions == 1:
                xf, yf = self.x - possible_move[directions], self.y + possible_move[directions]

            elif directions == 2:
                xf, yf = self.x - possible_move[directions], self.y - possible_move[directions]

            else:
                xf, yf = self.x + possible_move[directions], self.y - possible_move[directions]

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
        kingMoves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        movelist = []
        for i in range(8):
            xf = self.x + kingMoves[i][0]
            yf = self.y + kingMoves[i][1]
            if self.there_is_piece_between(xf, yf, board) == -1:
                pass
            if self.there_is_piece_between(xf, yf, board) == 0:  # não é uma peça aliada (pode ser peça vazia ou inimiga)
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

    def verify_if_black_pawn_can_go_2_squares(self, move):

<<<<<<< HEAD
        if move == (self.x, self.y - 2) and self.already_moved:
            return False

        else:
            return True

    def verify_if_white_pawn_can_go_2_squares(self, move):

        if move == (self.x, self.y + 2) and self.already_moved:
            return False

        else:
            return True

    def move(self, new_square, moveList):

        ans = True
        for move in moveList:

            if move == (new_square.x, new_square.y):

                if not (self.verify_if_black_pawn_can_go_2_squares(move)):
                    ans = False

                elif not (self.verify_if_white_pawn_can_go_2_squares(move)):
                    ans = False
                else:
                    self.already_moved = True
                return ans

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

                if self.isInRange(xf, yf):
                    # verificar se a peça é da mesma cor
                    if board[xf + yf * 8].returnPieceColor() != self._color:
                        moveList.append((xf, yf))  # append de uma tupla

        else:
            if self.already_moved:
                possible_moves = [(0, -1)]
            else:
                possible_moves = [(0, -1), (0, -2)]

            for move in possible_moves:
                xf = self.x + move[0]
                yf = self.y + move[1]

                if self.isInRange(xf, yf):
                    # verificar se a peça é da mesma cor
                    if board[xf + yf * 8].returnPieceColor() != self._color:
                        moveList.append((xf, yf))  # append de uma tupla

        return moveList
=======
  def moveList(self, board):
    return []
>>>>>>> 79beea113d86ba652c12178c62566fe510837e9d
