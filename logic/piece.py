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
        self.en_passant = False


class Knight(Piece):

    def __init__(self, color):
        super().__init__('knight', color, 3)

    @staticmethod
    def special_moves(column, row):
        return [(column + 2, row - 1), (column + 2, row + 1),
                (column + 1, row - 2), (column + 1, row + 2),
                (column - 1, row - 2), (column - 1, row + 2),
                (column - 2, row - 1), (column - 2, row + 1)]


class Bishop(Piece):

    def __init__(self, color):
        super().__init__('bishop', color, 3)

    @staticmethod
    def special_moves():
        return [(-1, -1), (1, -1),  # left-up, right-up
                (-1, 1), (1, 1)]    # left-down, right-down


class Rook(Piece):

    def __init__(self, color):
        super().__init__('rook', color, 5)

    @staticmethod
    def special_moves():
        return [(0, -1),            # up
                (-1, 0), (1, 0),    # left, right
                (0, 1)]             # down


class Queen(Piece):

    def __init__(self, color):
        super().__init__('queen', color, 9)

    @staticmethod
    def special_moves():
        return [(0, -1),            # up
                (-1, 0), (1, 0),    # left, right
                (0, 1),             # down
                (-1, -1), (1, -1),  # left-up, right-up
                (-1, 1), (1, 1)]    # left-down, right-down


class King(Piece):

    def __init__(self, color):
        super().__init__('king', color, 4)
        self.closer_rook = None
        self.further_rook = None

    @staticmethod
    def special_moves(column, row):
        return [(column - 1, row + 1), (column, row + 1), (column + 1, row + 1),
                (column - 1, row), (column + 1, row),
                (column - 1, row - 1), (column, row - 1), (column + 1, row - 1)]
