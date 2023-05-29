from logic.piece import *
from logic.allowed_moves import AllowedMoves
from logic.const import COLUMNS, ROWS
from logic.field import Field
from logic.move import Move


class Ending:

    def __init__(self, board):
        self.board = board
        self.who_won = None
        self.movements_without_capture = 0
        self.positions = {}
        self.i = 0

    def fifty_moves(self, piece, move):
        stop = move.stop
        if self.board.fields[stop.column][stop.row].is_not_empty() and isinstance(piece, Pawn):
            self.movements_without_capture = 0
        else:
            self.movements_without_capture += 1
        if self.movements_without_capture == 49:
            return True
        else:
            return False

    def stalemate(self, color):
        for column in range(COLUMNS):
            for row in range(ROWS):
                field = self.board.fields[column][row]
                if field.is_not_empty():
                    if field.piece.color == color:
                        if isinstance(field.piece, King):
                            king = field.piece
                            start = stop = Field(column, row)
                            move = Move(start, stop)
                            if AllowedMoves.under_check(king, move, self.board):
                                return False
                        if AllowedMoves.detect(field.piece, column, row, self.board, boolean=True):
                            return False
        return True

    def position_three_times(self, piece):
        if not isinstance(piece, Pawn):
            position = []
            for column in range(COLUMNS):
                col = []
                for row in range(ROWS):
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

    def insufficient_material(self):
        pieces = []
        for col in range(COLUMNS):
            for row in range(ROWS):
                if self.board.fields[col][row].is_not_empty():
                    pieces.append(str(self.board.fields[col][row].piece))
                if len(pieces) > 3:
                    return False
        if pieces.count("king") == 2:
            if pieces.count("knight") or pieces.count("bishop") or pieces.count("knight"):
                return True
            elif len(pieces) == 2:
                return True

    def checkmate(self, color):
        opponent_color = "black" if color == "white" else "white"
        for column in range(COLUMNS):
            for row in range(ROWS):
                field = self.board.fields[column][row]
                if field.is_not_empty():
                    if field.piece.color == opponent_color:
                        if AllowedMoves.detect(field.piece, column, row, self.board, True, True):
                            return False
        return True

    def check_result(self, piece, move):
        color = piece.color
        opponent_color = "black" if color == "white" else "white"
        if self.stalemate(color):
            return "Draw by stalemate."
        elif self.position_three_times(piece):
            return "{} won!".format(opponent_color)
        elif self.insufficient_material():
            return "Draw by insufficient material."
        elif self.checkmate(color):
            return "{} won!".format(color)
        elif self.fifty_moves(piece, move):
            return "Draw by fifty moves rule."
        else:
            return None

        # to add: announcement in return
