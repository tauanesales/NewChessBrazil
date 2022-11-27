import pyglet
from classes.Colors import Color
from typing import Any
from classes.Piece import *

class PromotionMenu(pyglet.window.Window):
    def __init__(self, gamestate: Any):
        self.ids = ["B", "N", "Q", "R"]
        self.images = {}
        self.chosen = None
        self.pieceSize = 64
        self.pieces = [Bishop, Knight, Queen, Rook]
        if gamestate.whiteToMove:

            self.color = Color.WHITE
        else:
            self.color = Color.BLACK

        # super().__init__(self.pieceSize*4, self.pieceSize)
        self.loadPieces()
        self.pawnObj = gamestate.promotedPawnObj

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
            self.chosen = self.pieces[0]
        elif self.pieceSize * 1 < x <= self.pieceSize * 2:
            self.chosen = self.pieces[1]

        elif self.pieceSize * 2 < x <= self.pieceSize * 3:
            self.chosen = self.pieces[2]

        else:
            self.chosen = self.pieces[3]

        self.pawnObj.chosenPromotedPiece = self.chosen

        return "game"
