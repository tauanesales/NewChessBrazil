import pyglet
import ChessEngine
from classes.MyWindow import MyWindow
from classes.Board import Board


def main() -> None:
    width = height = 512
    board = Board(width, height)
    gs = ChessEngine.GameState(board.board_rotation)
    running = True
    window = MyWindow(width, height, board, running, gs)
    pyglet.app.run()


if __name__ == "__main__":
    main()
