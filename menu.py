# importação de módulos do pyglet
import pyglet
import pyglet.window.key

width = 512 # largura da janela
height = 512 # altura da janela
title = "New Chess Brazil" # título da janela

window = pyglet.window.Window(width, height, title) # criação da janela
text1 = "DESAFIE SEU AMIGO NUMA" # texto na janela
text2 = "PARTIDA DE XADREZ" # texto na janela
New = "New" # texto na janela
Chess = "Chess" # texto na janela
Brazil = "Brazil" # texto na janela

label1 = pyglet.text.Label(text1, # criação de um rótulo com as devidas formatações
                          font_name='Comic Sans MS', # fonte do texto
                          font_size=15, # tamanho do texto
                          x=window.width//2, y=window.height - 30, # posição do texto na janela
                          anchor_x='center', anchor_y='center') # centralização do texto
label2 = pyglet.text.Label(text2,
                          font_name='Comic Sans MS',
                          font_size=15,
                          x=window.width//2, y=window.height - 55,
                          anchor_x='center', anchor_y='center')
labelN = pyglet.text.Label(New,
                          font_name='Comic Sans MS',
                          font_size=40,
                          x=window.width - 325, y=window.height - 150,
                          anchor_x='center', anchor_y='center')
labelN.color = (96, 169, 23, 255)
labelC = pyglet.text.Label(Chess,
                          font_name='Comic Sans MS',
                          font_size=40,
                          x=window.width - 205, y=window.height - 150,
                          anchor_x='center', anchor_y='center')
labelC.color = (227, 200, 0, 255)
labelB = pyglet.text.Label(Brazil,
                          font_name='Comic Sans MS',
                          font_size=40,
                          x=window.width//2, y=window.height - 190,
                          anchor_x='center', anchor_y='center')
labelB.color = (27, 161, 226, 255)

batch = pyglet.graphics.Batch() 
wallpaper = pyglet.image.load('public/capa.png')
imagebutton = pyglet.image.load('public/start.png')
sprite1 = pyglet.sprite.Sprite(wallpaper, x = 0, y = 0)
sprite2 = pyglet.sprite.Sprite(imagebutton, x = 200, y = 50)

@window.event # evento de desenho
def on_draw():
    window.clear() # limpa a janela
    sprite1.draw() # desenha sprite1 na janela
    sprite2.draw() # desenha sprite2 na janela
    label1.draw() # desenha label1 na janela
    label2.draw() # desenha label2 na janela
    labelN.draw() # desenha labelN na janela
    labelC.draw() # desenha labelC na janela
    labelB.draw() # desenha labelB na janela

@window.event # evento de pressionamento de tecla
def on_key_press(symbol, modifier):
    if symbol == pyglet.window.key.C: # se "C" for pressionado
        print('Inicia o jogo') # Imprime isso
    
    if symbol == pyglet.window.key.X: # se "X" for pressionado
        window.close() # fecha a janela

img = image = pyglet.resource.image("public/bN.png") # imagem para ícone da janela
window.set_icon(img) # definindo imagem como ícone

pyglet.app.run() # inicia a execução do aplicativo