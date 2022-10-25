import pyglet


class MyWindow(pyglet.window.Window):

    def __init__(self, width, height, board, running, gamestate):
        super().__init__(width, height, caption="Chess")
        self.board = board
        self.running = running
        self.gs = gamestate
        self.batch = self.board.batch

    def on_draw(self):

        if self.running:
            self.clear()
            self.batch.draw()  # desenhar batches devido ao alto número de shapes

            for line in self.board.board:  # desenhar as peças normalmente
                for square in line:
                    square.drawPiece()

    def on_mouse_press(self, x, y, button, modifiers):

        if self.gs.clicked == 0 or self.gs.clicked == 1:
            self.gs.clicked = self.board.pieceClick(x, y, self.gs.whiteToMove)

        else:
            old_i, old_j = self.gs.clicked
            i, j = self.board.squareClick(x, y)

            args = (i, j, old_i, old_j)

            if self.board.isSameColor(*args) == None:
                self.gs.clicked = self.board.noColorClick(*args)

            elif self.board.isSameColor(*args) == True:
                self.gs.clicked = self.board.sameColorClick(*args)

            else:
                self.gs.clicked = self.board.otherColorClick(*args)

            if self.gs.clicked == 1:
                self.gs.shiftChange()