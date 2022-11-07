import pyglet


class MyWindow(pyglet.window.Window):

    def __init__(self, width, height, board, running, gamestate):
        super().__init__(width, height, caption="Chess")
        self.board = board
        self.running = running
        self.gs = gamestate
        self.batch = self.board.batch
        self.drag = 0
        self.click_x = 0
        self.click_y = 0

    def boardSquare(self, i, j):
        return self.board.board[i][j]

    def drag_circle(self, x, y, value):
        return ((x - self.click_x)**2 + (y - self.click_y)**2) > value**2

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

            if type(self.gs.clicked) == tuple:
                self.click_x = x
                self.click_y = y

        else:
            old_i, old_j = self.gs.clicked
            i, j = self.board.squareClick(x, y)
            args = (i, j, old_i, old_j)

            if self.board.isSameColor(*args) is None:
                self.gs.clicked = self.board.noColorClick(*args, self.gs)

            elif self.board.isSameColor(*args) == True:
                self.gs.clicked = self.board.sameColorClick(*args)

            else:
                self.gs.clicked = self.board.otherColorClick(*args,self.gs)

            if self.gs.clicked == 1:
                self.gs.shiftChange()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if pyglet.window.mouse.LEFT and type(self.gs.clicked) == tuple:
            i, j = self.gs.clicked

            if self.drag_circle(x, y, 5) and self.drag == 0:
                yi, xi = self.board.returnSquareXY(i, j)
                self.click_x, self.click_y = x - xi, y -yi # delta x, delta y
                self.drag = 1

            elif self.drag == 1:
                self.boardSquare(i, j).changeImageCoord(x - self.click_x, y - self.click_y)

    def on_mouse_release(self, x, y, button, modifiers):
        if pyglet.window.mouse.LEFT and type(self.gs.clicked) == tuple:
            old_i, old_j = self.gs.clicked
            self.boardSquare(old_i, old_j).changeImageCoord()

            if self.drag == 1:
                self.on_mouse_press(x, y, button, modifiers)
                self.drag = 0
