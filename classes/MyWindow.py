import pyglet


class MyWindow(pyglet.window.Window):

    def __init__(self, width, height, board, running, gamestate, batch):
        super().__init__(width, height, caption="Chess")
        self.board = board
        self.running = running
        self.gs = gamestate
        self.batch = batch

    def on_draw(self):
        if self.running:
            self.clear()
            self.batch.draw()  # desenhar batches devido ao alto número de shapes

            for line in self.board:  # desenhar as peças normalmente
                for square in line:
                    square.drawPiece()

    def on_mouse_press(self, x, y, button, modifiers):

        if self.gs.clicked == 0:  # tabuleiro não clicado
            for line in self.board:
                for square in line:
                    if square.hasPiece(x, y) and square.onClick(self.gs,
                                                            self.board):  # se tiver peça na casa e se a peça é a mesma cor do turno atual
                        self.gs.clicked = square.returnCoordinates()  # em vez de retornar 1, melhor retornar as coordenadas da peça clicada

        else:
            for line in self.board:
                for new_square in line:
                    if new_square.returnPoint(x, y):  # verificar onde foi clicado
                        (i_initial, j_initial) = self.gs.clicked  # receber as coordenadas do gamestate para comparação
                        old_square = self.board[i_initial][j_initial]  # coords do tabuleiro antigo na lista do tabuleiro

                        if old_square.analyseMove(new_square, self.board, self.gs.rotation):
                            old_square.movePiece(new_square, self.board, self.gs.rotation)  # mover a peça de coordenada
                            self.gs.shiftChange()  # mudar turno
                            self.gs.clicked = 0  # retornar ao status 0

                        else:  # se não for possível mover para o lugar

                            if new_square.returnPieceColor() == old_square.returnPieceColor():  # se a peça clicada for da mesma cor
                                old_square.squareColorChange(self.board, self.gs.rotation)  # "retornar" a casa anterior à cor original
                                self.gs.clicked = 0

                                if new_square != old_square:  # se a peça clicada não for a mesma, para efetuar o clique na outra peça
                                    new_square.squareColorChange(self.board, self.gs.rotation)
                                    self.gs.clicked = new_square.returnCoordinates()

                            elif new_square.piece == None:  # se não houver peças na casa clicada, para "desclicar"
                                old_square.squareColorChange(self.board, self.gs.rotation)
                                self.gs.clicked = 0