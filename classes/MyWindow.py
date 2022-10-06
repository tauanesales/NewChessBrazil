import pyglet

class MyWindow(pyglet.window.Window):
  def __init__(self,width,height,board,pieces, running):
    super().__init__(width,height, caption = "Chess")
    self.board = board
    self.pieces = pieces
    self.running = running

  def on_draw(self):
    
    if self.running:

      self.clear()
      
      for rect in self.board:
        rect.draw()
      
      for piece in self.pieces:
        piece.draw()
    
  
  def on_mouse_press(self, x, y, button, modifiers):
    pass
