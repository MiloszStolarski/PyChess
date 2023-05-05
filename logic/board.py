import copy
from logic.const import ROWS, COLUMNS
from logic.field import Field
from logic.piece import *
from logic.move import Move
from visual.sound import Sound



class Board:

    def __init__(self):
        self.fields = [[Field(column, row) for column in range(COLUMNS)] for row in range(ROWS)]
        self.last_move = None
        self._test_board()
        #self._add_pieces('white')
        #self._add_pieces('black')

    def move(self, piece, move, remover=False):
        start = move.start
        stop = move.stop

        # en passant detect
        en_passant_empty = self.fields[stop.column][stop.row].is_empty()

        # board update
        self.fields[start.column][start.row].piece = None
        self.fields[stop.column][stop.row].piece = piece

        if isinstance(piece, Pawn):
            # en passant capture
            diff = stop.column - start.column
            if diff != 0 and en_passant_empty:
                self.fields[start.column + diff][start.row].piece = None
                self.fields[stop.column][stop.row].piece = piece
                if not remover:
                    sound = Sound(os.path.join(
                        'sounds/capture.wav'
                    ))
                    sound.play()

            self.check_promotion(piece, stop)

        # castling
        if isinstance(piece, King):
            if self.castling(start, stop) and not remover:
                diff = stop.column - start.column
                rook = piece.further_rook if (diff < 0) else piece.closer_rook
                self.move(rook, rook.moves[-1])

        piece.moved = True
        piece.clear_moves()

        self.last_move = move

    @staticmethod
    def valid_move(piece, move):
        return move in piece.moves

    def allowed_moves(self, piece, column, row, check_verify=True):
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
                        move = Move(start, stop)
                        if check_verify:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                    else:
                        break
                else:
                    break

            # capture piece
            possible_columns = [column - 1, column + 1]
            possible_row = row + piece.direction
            for possible_move in possible_columns:
                if Field.in_range(possible_move, possible_row):
                    if self.fields[possible_move][possible_row].is_opponent(piece.color):
                        start = Field(column, row)
                        final_piece = self.fields[possible_move][possible_row].piece
                        stop = Field(possible_move, possible_row, final_piece)
                        move = Move(start, stop)
                        if check_verify:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

            # en passant
            r = 3 if piece.color == 'white' else 4
            final_row = 2 if piece.color == 'white' else 5
            if Field.in_range(column - 1) and row == r:
                if self.fields[column - 1][r].is_opponent(piece.color):
                    p = self.fields[column - 1][row].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            start = Field(column, row)
                            stop = Field(column - 1, final_row, p)
                            move = Move(start, stop)
                            if check_verify:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

            if Field.in_range(column + 1) and row == r:
                if self.fields[column + 1][r].is_opponent(piece.color):
                    p = self.fields[column + 1][row].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            start = Field(column, row)
                            stop = Field(column + 1, final_row, p)
                            move = Move(start, stop)
                            if check_verify:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)


        def around_moves(possible_moves):
            for move in possible_moves:
                move_column, move_row = move
                if Field.in_range(move_column, move_row):
                    if self.fields[move_column][move_row].is_empty_or_is_opponent(piece.color):
                        # possible_move
                        start = Field(column, row)
                        final_piece = self.fields[move_column][move_row].piece
                        stop = Field(move_column, move_row, final_piece)
                        move = Move(start, stop)
                        if check_verify:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            else:
                                break
                        else:
                            piece.add_move(move)

        def longitudinal_moves(directions):
            start = Field(column, row)
            for direction in directions:
                column_dir, row_dir = direction
                stop_column = column
                stop_row = row
                while True:
                    stop_column += column_dir
                    stop_row += row_dir
                    """
                    if Field.in_range(stop_column, stop_row):
                        if self.fields[stop_column][stop_row].is_empty():
                            final_piece = self.fields[stop_column][stop_row].piece
                            stop = Field(stop_column, stop_row, final_piece)
                            move = Move(start, stop)
                            if check_verify:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                        elif self.fields[stop_column][stop_row].is_opponent(piece.color):
                            final_piece = self.fields[stop_column][stop_row].piece
                            stop = Field(stop_column, stop_row, final_piece)
                            move = Move(start, stop)
                            if check_verify:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            break
                        else:
                            break
                    """
                    if Field.in_range(stop_column, stop_row):
                        field = self.fields[stop_column][stop_row]
                        if field.is_empty_or_is_opponent(piece.color):
                            final_piece = field.piece
                            stop = Field(stop_column, stop_row, final_piece)
                            move = Move(start, stop)
                            if check_verify:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            if field.is_opponent(piece.color):
                                break


                    else:
                        break

        def king_moves(moves):
            # castling upgrade with checks and capture on king
            around_moves(king_normal_moves)
            if not piece.moved:
                closer_rook = self.fields[7][row].piece
                further_rook = self.fields[0][row].piece
                if isinstance(further_rook, Rook) and not further_rook.moved:
                    # checking if is piece between Rook and King
                    # to add check method
                    for c in range(1, 4):
                        if self.fields[c][row].is_not_empty():
                            break
                        if c == 3:
                            piece.further_rook = further_rook

                            start = Field(0, row)
                            stop = Field(3, row)
                            move_rook = Move(start, stop)
                            further_rook.add_move(move_rook)

                            start = Field(column, row)
                            stop = Field(2, row)
                            move_king = Move(start, stop)
                            piece.add_move(move_king)

                            if check_verify:
                                if not self.in_check(piece, move_king) and not self.in_check(further_rook, move_rook):
                                    piece.add_move(move_king)
                                    further_rook.add_move(move_rook)
                            else:
                                piece.add_move(move_king)
                                further_rook.add_move(move_rook)

                if isinstance(closer_rook, Rook) and not closer_rook.moved:
                    # checking if is piece between Rook and King
                    for c in range(5, 7):
                        if self.fields[c][row].is_not_empty():
                            break
                        if c == 6:
                            piece.closer_rook = closer_rook

                            start = Field(7, row)
                            stop = Field(5, row)
                            move_rook = Move(start, stop)
                            closer_rook.add_move(move_rook)

                            start = Field(column, row)
                            stop = Field(6, row)
                            move_king = Move(start, stop)
                            piece.add_move(move_king)

                            if check_verify:
                                if not self.in_check(piece, move_king) and not self.in_check(further_rook, move_rook):
                                    piece.add_move(move_king)
                                    further_rook.add_move(move_rook)
                            else:
                                piece.add_move(move_king)
                                further_rook.add_move(move_rook)

        # ---------------------------- #
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
            king_normal_moves = [
                (column - 1, row + 1), (column, row + 1), (column + 1, row + 1),
                (column - 1, row), (column + 1, row),
                (column - 1, row - 1), (column, row - 1), (column + 1, row - 1),
            ]
            king_moves(king_normal_moves)

    def check_promotion(self, piece, stop):
        if stop.row == 0 or stop.row == 7:
            self.fields[stop.column][stop.row].piece = Queen(piece.color)

    def castling(self, start, stop):
        return abs(start.column - stop.column) == 2

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, remover=True)

        for column in range(COLUMNS):
            for row in range(ROWS):
                if temp_board.fields[column][row].is_opponent(piece.color):
                    opponent = temp_board.fields[column][row].piece
                    temp_board.allowed_moves(opponent, column, row, check_verify=False)
                    for opponent_move in opponent.moves:
                        if isinstance(opponent_move.stop.piece, King):
                            return True
        return False

    def en_passant_set(self, piece):
        if not isinstance(piece, Pawn):
           return
        for column in range(COLUMNS):
            for row in range(ROWS):
                if isinstance(self.fields[column][row].piece, Pawn):
                    self.fields[column][row].piece.en_passant = False
        piece.en_passant = True

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # add pawns
        for column in range(COLUMNS):
            self.fields[column][row_pawn].piece = Pawn(color)


        # add knights
        self.fields[1][row_other].piece = Knight(color)
        self.fields[6][row_other].piece = Knight(color)


        # add bishops
        self.fields[2][row_other].piece = Bishop(color)
        self.fields[5][row_other].piece = Bishop(color)

        # to delete
        """
        self.fields[0][5].piece = Pawn(color)
        self.fields[7][5].piece = Bishop(color)
        self.fields[4][4].piece = Rook(color)
        self.fields[6][5].piece = Queen(color)
        self.fields[4][5].piece = King(color)
        self.fields[3][3].piece = Knight(color)
        """
        # add rooks
        self.fields[0][row_other].piece = Rook(color)
        self.fields[7][row_other].piece = Rook(color)

        # add queen
        self.fields[3][row_other].piece = Queen(color)

        # add king
        self.fields[4][row_other].piece = King(color)

    def _test_board(self):
        self.fields[3][4].piece = King('white')
        self.fields[3][5].piece = Queen('white')

        self.fields[3][2].piece = King('black')
        self.fields[3][1].piece = Queen('black')
