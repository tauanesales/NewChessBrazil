import pyglet
import ChessEngine
from classes.MyWindow import MyWindow
from classes.Board import Board

def main():
    width = height = 512

    board = Board(width, height)

    gs = ChessEngine.GameState(board.board_rotation)  # adicionando o gamestate ao jogo

    running = True  # "rodar" o jogo

    window = MyWindow(width, height, board, running, gs)  # criação da janela

    pyglet.app.run()


if __name__ == "__main__":
    main()
