import pyglet

class CheckMateMenu:
  def __init__(self,width,height):
    self.width = width 
    self.height = height
    self.checkmateWarning = pyglet.text.Label("Checkmate", # criação de um rótulo com as devidas formatações
                                font_name='Comic Sans MS', # fonte do texto
                                font_size=15, # tamanho do texto
                                x=self.width//2, y=self.height//2, # posição do texto na janela
                                anchor_x='center', anchor_y='center') # centralização do texto
  

  def on_draw(self):
    self.checkmateWarning.draw()