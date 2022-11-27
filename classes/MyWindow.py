import pyglet
from StartMenu import StartMenu
from CheckMateMenu import CheckMateMenu

class MyWindow(pyglet.window.Window):

    def __init__(self, width, height, board, running, gamestate,window = "start"):
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
        self.window = window
        self.startMenu = StartMenu(width, height, "New Chess Brazil")
        self.checkmateMenu = CheckMateMenu(width,height)

    def boardSquare(self, i, j):
        return self.board.board[i][j]

    def drag_circle(self, x, y, value):
        return ((x - self.click_x)**2 + (y - self.click_y)**2) > value**2

    def on_draw(self):
        self.clear()
        if self.gs.checkMate:
            self.checkmateMenu.on_draw()
        else:
            if self.window == "game":
                self.on_draw_game_menu()
            elif self.window == "start":
                self.startMenu.on_draw()

    def on_draw_game_menu(self):
        if self.running:
            
            self.batch.draw()  # desenhar batches devido ao alto número de shapes

            for line in self.board.board:  # desenhar as peças normalmente
                for square in line:
                    square.drawPiece()
                
    def on_mouse_press(self, x, y, button, modifiers):
        if self.window == "game":
            self.on_mouse_press_game_window(x, y, button, modifiers)

    def on_mouse_press_game_window(self,x, y, button, modifiers):
        self.click_x = x
        self.click_y = y
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.window == "game":
            self.on_mouse_drag_game_window(x, y, dx, dy, buttons, modifiers)


    def on_mouse_drag_game_window(self, x, y, dx, dy, buttons, modifiers):
        if pyglet.window.mouse.LEFT:

            if self.drag_circle(x, y, 5) and self.drag == 0:
                coord = self.board.pieceClick(self.click_x, self.click_y, self.gs)

                if type(coord) == tuple:
                    (i, j) = coord
                    yi, xi = self.board.returnSquareXY(i, j)
                    self.delta_x, self.delta_y = x - xi, y -yi
                    self.board.dragSquareSwitch(coord, self.gs)
                    self.gs.clicked = coord
                    self.drag = 1

            elif self.drag == 1:
                i, j = self.board.squareClick(self.click_x, self.click_y)
                self.boardSquare(i, j).changeImageCoord(x - self.delta_x, y - self.delta_y)


    def on_mouse_release(self, x, y, button, modifiers):
        if self.window == "game":
            self.on_mouse_release_game_window(x, y, button, modifiers)
        elif self.window == "start":
            self.window = self.startMenu.on_mouse_release(x, y, button, modifiers)


    def on_mouse_release_game_window(self, x, y, button, modifiers):
        if pyglet.window.mouse.LEFT:
            if self.drag == 0 and type(self.gs.clicked) == int:
                self.gs.clicked = self.board.pieceClick(x, y, self.gs)

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
                        self.gs.clicked = self.board.noColorClick(*args, self.gs)

                    elif self.board.isSameColor(*args) == True:
                        self.gs.clicked = self.board.sameColorClick(*args, self.drag, self.gs)

                    else:
                        self.gs.clicked = self.board.otherColorClick(*args, self.gs)

                    if self.gs.clicked == 1:
                        self.gs.shiftChange(self.board)

            if self.drag == 1:
                self.drag = 0

            if self.gs.checkMate:
                self.running = False
