"""
This is our main driver file. resposible for handling user input and displaying the current GameState
"""

import pyglet
import ChessEngine
from classes.MyWindow import MyWindow
from classes.Piece import *
from classes.Board import Square

width = height = 512 # tamanho do tabuleiro
dimension = 8 # tabuleiro 8x8
square_size = height // dimension # tamanho do quadrado
max_fps = 15
images = {} # dict de sprites das peças
batch = pyglet.graphics.Batch() # batch para renderizar com mais eficiência
sprites = [] # lista dos shapes da casa para renderização (batch)

def loadImages():
  pieces = ["bR","bN","bB","bQ","bK","bB","bN","bR","bp","wp","wR","wN","wB","wQ","wK","wB","wN","wR"]

  for piece in pieces:
    images[piece] = pyglet.image.load("public/" + piece + ".png")

"""
the main driver for our code. This will handle user inputs and updating the graphics
"""

def createBoard():
  colors = [(255,255,255),(128,128,128)]
  board = []
  for j in range(dimension):
    for i in range(dimension):
      color = colors[(i+(7-j)) % 2]
      rectangle = pyglet.shapes.Rectangle(x = square_size*i, y = square_size*j, batch = batch,
                                          width = square_size, height = square_size, color = color) # uso do batch, vários shapes
      sprites.append(rectangle)
      square = Square(rectangle, i, j, square_size, square_size) # instância da casa
      board.append(square) # adicionar à lista/"matriz"
  return board



"""
Draw the pieces on the board acording to the current GameState.board
"""
def createPieces(initial_board, object_board):

  for row in range(dimension):

    for col in range(dimension):

      piece = initial_board[7-row][col] # coordenada da matriz inicial do gamestate, conversão para o pyglet
      if piece != "--":
        piece_image = pyglet.sprite.Sprite(images[piece], x=col * square_size, y= (row * square_size)) # sprite da imagem
        args = (piece_image, piece, square_size, square_size, col, row) # construtor da classe das peças
        piece_instance = "" # instância da peça
        if piece[1] == "R":
          piece_instance = Rook(*args)
        elif piece[1] == "N":
          piece_instance = Knight(*args)
        elif piece[1] == "B":
          piece_instance = Bishop(*args)
        elif piece[1] == "Q":
          piece_instance = Queen(*args)
        elif piece[1] == "K":
          piece_instance = King(*args)
        elif piece[1] == "p":
          piece_instance = Pawn(*args)
        object_board[8*row + col].piece = piece_instance # vincular a peça à casa (lista linear)
  return object_board

def main():
  
  gs = ChessEngine.GameState()

  loadImages()

  running = True

  board = createPieces(gs.board, createBoard()) #Draws the squares on the board

  window = MyWindow(width, height, board, running, gs, batch)

  pyglet.app.run()

if __name__ == "__main__":
  main()