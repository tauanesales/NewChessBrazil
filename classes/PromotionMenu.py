import pyglet
from classes.Colors import Color

class PromotionMenu(pyglet.window.Window):
    def __init__(self, color):
        self.ids = ["B", "N", "Q", "R"]
        self.images = {}
        self.chosen = None
        self.pieceSize = 64
        self.color = color
        super().__init__(self.pieceSize*4, self.pieceSize)
        self.loadPieces()

    def loadPieces(self):
        i = 0
        if self.color == Color.WHITE:

            for id in self.ids:
                piece = "w" + id
                self.images[piece] = pyglet.image.load("public/" + piece + ".png")
                self.images[piece] = pyglet.sprite.Sprite(self.images[piece], x=i * self.pieceSize, y=0)
                i += 1
        else:
            for id in self.ids:
                piece = "b" + id
                self.images[piece] = pyglet.image.load("public/" + piece + ".png")
                self.images[piece] = pyglet.sprite.Sprite(self.images[piece], x=i * self.pieceSize, y=0)
                i += 1

    def on_draw(self):
        self.clear()

        for piece in self.images:
            self.images[piece].draw()

    def on_mouse_release(self, x, y, buttons, modifiers):
        if 0 <= x <= self.pieceSize * 1:
            self.chosen = 0

        elif self.pieceSize * 1 < x <= self.pieceSize * 2:
            self.chosen = 1

        elif self.pieceSize * 2 < x <= self.pieceSize * 3:
            self.chosen = 2

        else:
            self.chosen = 3

        self.close()

    def on_close(self):
        return self.chosen


