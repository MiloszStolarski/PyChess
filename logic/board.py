from logic.const import ROWS, COLUMNS
from logic.field import Field
from logic.piece import *
from logic.move import Move


class Board:

    def __init__(self):
        self.fields = [[Field(column, row) for column in range(COLUMNS)] for row in range(ROWS)]
        self.last_move = None

        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move):
        start = move.start
        stop = move.stop

        self.fields[start.column][start.row].piece = None
        self.fields[stop.column][stop.row].piece = piece

        piece.moved = True
        piece.clear_moves()     # nie kasuje ruchow innych pionkow po kazdym ruchu

        self.last_move = move

    @staticmethod
    def valid_move(piece, move):
        return move in piece.moves

    def allowed_moves(self, piece, column, row):
        """Check possible moves for piece"""
        piece.clear_moves()

        def pawn_moves():
            allowed_steps = 1 if piece.moved else 2

            # straight moves
            begin = row + piece.direction
            end = row + (piece.direction * (1 + allowed_steps))
            for possible_move in range(begin, end, piece.direction):
                if Field.in_range(possible_move):
                    if self.fields[column][possible_move].is_empty():
                        start = Field(column, row)
                        stop = Field(column, possible_move)
                        piece.add_move(Move(start, stop))
                    else:
                        break

            # capture piece
            possible_columns = [column - 1, column + 1]
            possible_row = row + piece.direction
            for possible_move in possible_columns:
                if Field.in_range(possible_move, possible_row):
                    if self.fields[possible_move][possible_row].is_opponent(piece.color):
                        start = Field(column, row)
                        stop = Field(possible_move, possible_row)
                        piece.add_move(Move(start, stop))

        def around_moves(possible_moves):
            for move in possible_moves:
                move_column, move_row = move
                if Field.in_range(move_column, move_row):
                    if self.fields[move_column][move_row].is_empty_or_is_opponent(piece.color):
                        # possible_move
                        start = Field(column, row)
                        stop = Field(move_column, move_row)
                        piece.add_move(Move(start, stop))

        def longitudinal_moves(directions):
            start = Field(column, row)
            for direction in directions:
                column_dir, row_dir = direction
                stop_column = column
                stop_row = row
                while True:
                    stop_column += column_dir
                    stop_row += row_dir
                    if Field.in_range(stop_column, stop_row):
                        if self.fields[stop_column][stop_row].is_empty():
                            stop = Field(stop_column, stop_row)
                            piece.add_move(Move(start, stop))
                        elif self.fields[stop_column][stop_row].is_opponent(piece.color):
                            stop = Field(stop_column, stop_row)
                            piece.add_move(Move(start, stop))
                            break
                        else:
                            # (is_mine)
                            break
                    else:
                        break

        # -------------- #
        if isinstance(piece, Pawn):
            pawn_moves()
        elif isinstance(piece, Knight):
            around_moves([
                (column + 2, row - 1), (column + 2, row + 1),
                (column + 1, row - 2), (column + 1, row + 2),
                (column - 1, row - 2), (column - 1, row + 2),
                (column - 2, row - 1), (column - 2, row + 1)
            ])
        elif isinstance(piece, Bishop):
            longitudinal_moves([
                (-1, -1), (1, -1),  # left-up, right-up
                (-1, 1), (1, 1)     # left-down, right-down
            ])
        elif isinstance(piece, Rook):
            longitudinal_moves([
                (0, -1),            # up
                (-1, 0), (1, 0),    # left, right
                (0, 1)              # down
            ])
        elif isinstance(piece, Queen):
            longitudinal_moves([
                (0, -1),            # up
                (-1, 0), (1, 0),    # left, right
                (0, 1),             # down
                (-1, -1), (1, -1),  # left-up, right-up
                (-1, 1), (1, 1)     # left-down, right-down
            ])
        elif isinstance(piece, King):
            around_moves([
                (column - 1, row + 1), (column, row + 1), (column + 1, row + 1),
                (column - 1, row), (column + 1, row),
                (column - 1, row - 1), (column, row - 1), (column + 1, row - 1),
            ])

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # add pawns
        for column in range(COLUMNS):
            self.fields[column][row_pawn].piece = Pawn(color)
        self.fields[0][5].piece = Pawn(color)

        # add knights
        self.fields[1][row_other].piece = Knight(color)
        self.fields[6][row_other].piece = Knight(color)
        self.fields[3][3].piece = Knight(color)

        # add bishops
        self.fields[2][row_other].piece = Bishop(color)
        self.fields[5][row_other].piece = Bishop(color)

        # to delete
        self.fields[7][5].piece = Bishop(color)
        self.fields[4][4].piece = Rook(color)
        self.fields[6][5].piece = Queen(color)
        self.fields[4][5].piece = King(color)

        # add rooks
        self.fields[0][row_other].piece = Rook(color)
        self.fields[7][row_other].piece = Rook(color)

        # add queen
        self.fields[3][row_other].piece = Queen(color)

        # add king
        self.fields[4][row_other].piece = King(color)