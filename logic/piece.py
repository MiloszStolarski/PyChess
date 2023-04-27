import os
from logic.const import DEFAULT_SIZE


class Piece:

    def __init__(self, name, color, value, image_rect=None):
        self.name = name
        self.color = color
        self.value = value
        self.image_path = None
        self.set_image()
        self.image_rect = image_rect
        self.moves = []
        self.moved = False

    def set_image(self, size=DEFAULT_SIZE):
        self.image_path = os.path.join(
            f'images/images_{size}px/{self.name}_{self.color}.png'
        )

    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []


class Pawn(Piece):

    def __init__(self, color):
        super().__init__('pawn', color, 1)
        self.direction = -1 if color == 'white' else 1


class Knight(Piece):

    def __init__(self, color):
        super().__init__('knight', color, 3)


class Bishop(Piece):

    def __init__(self, color):
        super().__init__('bishop', color, 3)


class Rook(Piece):

    def __init__(self, color):
        super().__init__('rook', color, 5)


class Queen(Piece):
    # powinna byc z rook i bishopa

    def __init__(self, color):
        super().__init__('queen', color, 9)


class King(Piece):

    def __init__(self, color):
        super().__init__('king', color, 4)
