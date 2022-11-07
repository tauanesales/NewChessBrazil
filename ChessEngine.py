class GameState():

    def __init__(self):
        self.whiteToMove = True  # turno das brancas
        self.clicked = 0  # verifica a peça que foi clicada
        self.moveLog = []
        self.check = False

    def shiftChange(self):  # mudança de turno
        if self.whiteToMove == True:
            self.whiteToMove = False
        else:
            self.whiteToMove = True
