from logic.piece import *
from logic.allowed_moves import AllowedMoves


class Ending:

    def __init__(self, board):
        self.board = board
        self.who_won = None
        self.movements_without_capture = 0
        self.positions = {}

    def fifty_moves(self, piece, move):
        """ 50 moves without capturing and pawn movement """
        stop = move.stop
        if self.board.fields[stop.column][stop.row].is_not_empty() and isinstance(piece, Pawn):
            self.movements_without_capture = 0
        else:
            self.movements_without_capture += 1
        if self.movements_without_capture == 49:
            return True
        else:
            return False

    def stalemate(self):
        color = self.board.which_move
        king = None
        for field in self.board.fields:
            if field.piece.color == color:
                if isinstance(field.piece, King):
                    king = field.piece
                if field.piece.moves:
                    return False
        if AllowedMoves.under_check(king, None, self.board):
            return False
        return True

    def position_three_times(self, piece):
        if not isinstance(piece, Pawn):
            position = []
            for column in self.board.fields:
                col = []
                for row in column:
                    col.append(str(self.board.fields[column][row].piece))
                position.append(tuple(col))
            position = tuple(position)

            if position in self.positions:
                self.positions[position] += 1
            else:
                self.positions[position] = 0

            if self.positions[position] == 2:
                return True
            return False

    """
    To add:
    - normal win
    - insufficient material
    - sum method
    """


    def check_result(self, piece, move):
        pass
