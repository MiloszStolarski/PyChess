import pygame
from logic.const import ENLARGED_SIZE


class Dragger:

    def __init__(self):
        self.dragging = False
        self.dragged_piece = None
        self.initial_coords = (0, 0)
        self.mouse_coords = (0, 0)

    def save_coords(self, coords):
        self.initial_coords = (coords[0], coords[1])

    def update_mouse(self, coords):
        self.mouse_coords = (coords[0], coords[1])

    def drag_piece(self, piece):
        self.dragged_piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.dragged_piece = None
        self.dragging = False

    def allow_piece_dragging(self, screen):
        """Zoom in on the chess piece and make it follow the mouse"""

        self.dragged_piece.set_image(ENLARGED_SIZE)
        image = pygame.image.load(self.dragged_piece.image_path)
        self.dragged_piece.image_rect = image.get_rect(center=self.mouse_coords)
        screen.blit(image, self.dragged_piece.image_rect)
