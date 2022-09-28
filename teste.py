
import pyglet
import ChessEngine


width = height = 512 #400 is another option
dimension = 8 #8x8 chess board
square_size = height // dimension
max_fps = 15 #for animations
images = {}



def loadImages():
  pieces = ["bR","bN","bB","bQ","bK","bB","bN","bR","bp","wp","wR","wN","wB","wQ","wK","wB","wN","wR"]

  for piece in pieces:
    images[piece] = pyglet.image.load("public/" + piece + ".png").get_region(width = square_size, height = square_size)
  
  # We can access an image by saying images[wp]


window = pyglet.window.Window()

@window.event
def on_draw():
  images[0]