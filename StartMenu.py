# importação de módulos do pyglet
import pyglet
import pyglet.window.key
from typing import Any

width = 512 # largura da janela
height = 512 # altura da janela
title = "New Chess Brazil" # título da janela


class StartMenu():
    def __init__(self,width: int, height: int, title: str) -> None:
        
        self.width = width 
        self.height = height
        self.title = title
        self.text1 = "DESAFIE SEU AMIGO NUMA" # texto na janela
        self.text2 = "PARTIDA DE XADREZ" # texto na janela
        self.New = "New" # texto na janelaself.
        self.Chess = "Chess" # texto na janela
        self.Brazil = "Brazil" # texto na janela
        self.batch = pyglet.graphics.Batch() 
        self.wallpaper = pyglet.image.load('public/capa.png')
        self.imagebutton = pyglet.image.load('public/start.png')
        self.sprite1 = pyglet.sprite.Sprite(self.wallpaper, x = 0, y = 0)
        self.sprite2 = pyglet.sprite.Sprite(self.imagebutton, x = 200, y = 80)
        self.label1 = pyglet.text.Label(self.text1, # criação de um rótulo com as devidas formatações
                                font_name='Comic Sans MS', # fonte do texto
                                font_size=15, # tamanho do texto
                                x=self.width//2, y=self.height - 30, # posição do texto na janela
                                anchor_x='center', anchor_y='center') # centralização do texto
        self.label2 = pyglet.text.Label(self.text2,
                                font_name='Comic Sans MS',
                                font_size=15,
                                x=self.width//2, y=self.height - 55,
                                anchor_x='center', anchor_y='center')
        self.labelN = pyglet.text.Label(self.New,
                                font_name='Comic Sans MS',
                                font_size=40,
                                x=self.width - 325, y=self.height - 150,
                                anchor_x='center', anchor_y='center')
        self.labelN.color = (96, 169, 23, 255)
        self.labelC = pyglet.text.Label(self.Chess,
                                font_name='Comic Sans MS',
                                font_size=40,
                                x=self.width - 205, y=self.height - 150,
                                anchor_x='center', anchor_y='center')
        self.labelC.color = (227, 200, 0, 255)
        self.labelB = pyglet.text.Label(self.Brazil,
                                font_name='Comic Sans MS',
                                font_size=40,
                                x=self.width//2, y=self.height - 190,
                                anchor_x='center', anchor_y='center')
        self.labelB.color = (27, 161, 226, 255)

    
    def on_draw(self) -> None: 
        
        self.sprite1.draw() # desenha sprite1 na janela
        self.sprite2.draw() # desenha sprite2 na janela
        self.label1.draw() # desenha label1 na janela
        self.label2.draw() # desenha label2 na janela
        self.labelN.draw() # desenha labelN na janela
        self.labelC.draw() # desenha labelC na janela
        self.labelB.draw() # desenha labelB na janela

    def on_mouse_release(self, x: int, y: int, button: Any, modifiers: Any) -> str:
        if self.startedButtonClicked(x,y):
            return "game"
        else:
            return "start"

    def startedButtonClicked(self, x: int, y: int) -> bool:

        return self.sprite2.x <= x <= self.sprite2.x + 112 and \
        self.sprite2.y <= y <= self.sprite2.y + 51
        
