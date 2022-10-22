from enum import Enum


class sColor(Enum): # cores para customizar o tabuleiro (até implementar outros métodos)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    CLICKED = (0, 200, 0)
    MOVEMENT = (200, 200, 200)
    MOVEMENT2 = (100, 100, 100)
    CAPTURE = (20, 100, 35)


class Color(Enum): # uso do enum para as cores
    WHITE = 1
    BLACK = 2
