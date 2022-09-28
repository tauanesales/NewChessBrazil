"""
This is our main driver file. resposible for handling user input and displaying the current GameState
"""

import pyglet
import ChessEngine


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

"""
Responsible for all the graphics within a current state
"""

def drawGameState(window,gs):
  drawBoard(window) #Draws the squares on the board 
  
  #add in highlighting or move suggestions (later)

  #drawPieces(window,gs.board) #Draws the pieces on top of those squares


def drawBoard(window):
  colors = [(255,255,255),(128,128,128)]
  board = []
  for i in range(dimension):
    for j in reversed(range(dimension)):
      
      color = colors[(i+(7-j)) % 2]
      rectangle = pyglet.shapes.Rectangle(x = square_size*i, y = square_size*j, width = square_size, height = square_size, color = color)
      board.append(rectangle)
      
  @window.event
  def on_draw():
    window.clear()
  
    for rect in board:
      rect.draw()
    



"""
Draw the pieces on the board acording to the current GameState.board
"""
def drawPieces(window, board):
  
  pieces = []
  for row in range(dimension):
    for col in range(dimension):
      piece = board[row][col]

      if piece != "--":
        piece_image = pyglet.sprite.Sprite(images[piece], x = row*square_size, y = col*square_size)
        
        pieces.append(piece_image)

  @window.event
  def on_draw():
    for piece in pieces:
      piece.draw()


def main():
  window = pyglet.window.Window(width,height)
  gs = ChessEngine.GameState()
  loadImages()


  drawGameState(window,gs)

  pyglet.app.run()

if __name__ == "__main__":
  main()