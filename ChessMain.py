"""
This is our main driver file. resposible for handling user input and displaying the current GameState
"""

import pyglet
import ChessEngine
from classes.MyWindow import MyWindow


width = height = 512 #400 is another option
dimension = 8 #8x8 chess board
square_size = height // dimension
max_fps = 15 #for animations
images = {}

"""
Initialize a global dictionary of images
"""

def loadImages():
  pieces = ["bR","bN","bB","bQ","bK","bB","bN","bR","bp","wp","wR","wN","wB","wQ","wK","wB","wN","wR"]

  for piece in pieces:
    images[piece] = pyglet.image.load("public/" + piece + ".png")
  
  # We can access an image by saying images[wp]


"""
the main driver for our code. This will handle user inputs and updating the graphics
"""



def createBoard():
  colors = [(255,255,255),(128,128,128)]
  board = []
  for i in range(dimension):
    for j in reversed(range(dimension)):
      
      color = colors[(i+(7-j)) % 2]
      rectangle = pyglet.shapes.Rectangle(x = square_size*i, y = square_size*j, width = square_size, height = square_size, color = color)
      board.append(rectangle)
      
  return board



"""
Draw the pieces on the board acording to the current GameState.board
"""
def createPieces(board):
  
  pieces = []
 
  for row in range(dimension):

    for col in range(dimension):
      

      piece = board[row][col]
      if piece != "--":
        piece_image = pyglet.sprite.Sprite(images[piece], x = col*square_size, y = (7-row)*square_size)
          
        pieces.append(piece_image)

   
  return pieces


def main():
  
  gs = ChessEngine.GameState()
  loadImages()
  running = True

  board = createBoard() #Draws the squares on the board 
  
  #add in highlighting or move suggestions (later)

  pieces = createPieces(gs.board) #Draws the pieces on top of those squares

  
  window = MyWindow(width,height,board,pieces,running)


  pyglet.app.run()

if __name__ == "__main__":
  main()