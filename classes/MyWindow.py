import pyglet

class MyWindow(pyglet.window.Window):
    def __init__(self, width, height, board, running, gamestate, batch):
        super().__init__(width, height, caption="Chess")
        self.board = board
        self.running = running
        self.gamestate = gamestate
        self.batch = batch

    def on_draw(self):

        if self.running:

            self.clear()

            self.batch.draw()  # desenhar batches devido ao alto número de shapes

            for rect in self.board:  # desenhar as peças normalmente
                rect.drawPiece()

    def on_mouse_press(self, x, y, button, modifiers):

        if self.gamestate.clicked == 0:  # tabuleiro não clicado

            for rect in self.board:
                if rect.hasPiece(x, y) and rect.onClick(self.gamestate,
                                                        self.board):  # se tiver peça na casa e se a peça é a mesma cor do turno atual
                    self.gamestate.clicked = rect.returnCoordinates()  # em vez de retornar 1, melhor retornar as coordenadas da peça clicada

        else:
            for new_square in self.board:
                if new_square.returnPoint(x, y):  # verificar onde foi clicado
                    xf, yf = new_square.returnCoordinates()  # coordenadas novas/finais
                    (xi, yi) = self.gamestate.clicked  # receber as coordenadas do gamestate para comparação
                    old_square = self.board[xi + yi * 8]  # coords do tabuleiro antigo na lista do tabuleiro
                    if old_square.analyseMove(new_square, self.board):  # verificar se é possível mover
                        old_square.movePiece(new_square, self.board)  # mover a peça de coordenada
                        new_square.changeImageCoord(xf, yf)  # mudar as coordenadas do sprite da peça
                        self.gamestate.shiftChange()  # mudar turno
                        self.gamestate.clicked = 0  # retornar ao status 0
                    else:  # se não for possível mover para o lugar
                        if new_square.returnPieceColor() == old_square.returnPieceColor():  # se a peça clicada for da mesma cor
                            old_square.squareColorChange(self.board)  # "retornar" a casa anterior à cor original
                            self.gamestate.clicked = 0
                            if new_square != old_square:  # se a peça clicada não for a mesma, para efetuar o clique na outra peça
                                new_square.squareColorChange(self.board)
                                self.gamestate.clicked = new_square.returnCoordinates()
                        elif new_square.piece == None:  # se não houver peças na casa clicada, para "desclicar"
                            old_square.squareColorChange(self.board)
                            self.gamestate.clicked = 0
                        else:  # caso a peça for da outra cor, não é necessário, mas caso queira remover
                            pass