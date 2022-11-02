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
        self.delta_x = 0
        self.delta_y = 0

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
        self.click_x = x
        self.click_y = y

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if pyglet.window.mouse.LEFT:

            if self.drag_circle(x, y, 5) and self.drag == 0:
                coord = self.board.pieceClick(self.click_x, self.click_y, self.gs.whiteToMove)

                if type(coord) == tuple:
                    (i, j) = coord
                    yi, xi = self.board.returnSquareXY(i, j)
                    self.delta_x, self.delta_y = x - xi, y -yi
                    self.board.dragSquareSwitch(coord, self.gs.clicked)
                    self.gs.clicked = coord
                    self.drag = 1

            elif self.drag == 1:
                i, j = self.board.squareClick(self.click_x, self.click_y)
                self.boardSquare(i, j).changeImageCoord(x - self.delta_x, y - self.delta_y)


    def on_mouse_release(self, x, y, button, modifiers):
        if pyglet.window.mouse.LEFT:
            if self.drag == 0 and type(self.gs.clicked) == int:
                self.gs.clicked = self.board.pieceClick(x, y, self.gs.whiteToMove)

            elif type(self.gs.clicked) == tuple:
                old_i, old_j = self.gs.clicked
                self.boardSquare(old_i, old_j).changeImageCoord()

                try:
                    i, j = self.board.squareClick(x, y)

                except TypeError:
                    pass

                else:
                    args = (i, j, old_i, old_j)

                    if self.board.isSameColor(*args) is None:
                        self.gs.clicked = self.board.noColorClick(*args)

                    elif self.board.isSameColor(*args) == True:
                        self.gs.clicked = self.board.sameColorClick(*args, self.drag)

                    else:
                        self.gs.clicked = self.board.otherColorClick(*args)

                    if self.gs.clicked == 1:
                        self.gs.shiftChange()

            if self.drag == 1:
                self.drag = 0
