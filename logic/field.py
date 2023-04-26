
class Field:

    ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    def __init__(self, column, row, piece=None):
        self.column = column
        self.row = row
        self.piece = piece
        self.alphacol = self.ALPHACOLS[column]

    def __str__(self):
        return f"Field[{self.column} {self.row}]"

    def __eq__(self, other):
        return self.column == other.column and self.row == other.row


    def is_empty(self):
        return self.piece is None

    def is_not_empty(self):
        return self.piece is not None

    def is_opponent(self, color):
        return self.piece is not None and self.piece.color != color

    def is_mine(self, color):
        return self.piece is not None and self.piece.color == color

    def is_empty_or_is_opponent(self, color):
        return self.is_empty() or self.is_opponent(color)

    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True

    @staticmethod
    def get_alphacol(column):
        ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        return ALPHACOLS[column]