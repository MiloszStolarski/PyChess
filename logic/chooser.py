import pygame
import piece
from const import SQ_SIZE


class Chooser:

    def __init__(self):
        self.choosing = False
        self.chose = None
        self.choose_coords = (0, 0)
        self.mouse_cords = (0, 0)

    def choosing_piece(self, screen, color, field):
        column = field.column
        row = field.row + 1 if field.row == 0 else field.row - 1
        rect = (column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE * 0.85, SQ_SIZE * 0.85)
        pygame.draw.rect(screen, 'grey', rect)




