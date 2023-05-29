from logic.field import Field
from logic.piece import *
from logic.move import Move
from logic.const import COLUMNS, ROWS
import copy
from visual.sound import Sound


class AllowedMoves:

    @staticmethod
    def detect(piece, column, row, board, check_verify=True, boolean=False):
        """Check possible moves for piece"""

        def around_moves(possible_moves):
            for move in possible_moves:
                move_column, move_row = move
                if Field.in_range(move_column, move_row):
                    if board.fields[move_column][move_row].is_empty_or_is_opponent(piece.color):
                        start = Field(column, row)
                        final_piece = board.fields[move_column][move_row].piece
                        stop = Field(move_column, move_row, final_piece)
                        move = Move(start, stop)
                        if check_verify:
                            if not AllowedMoves.under_check(piece, move, board):
                                piece.add_move(move)
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
                    if Field.in_range(stop_column, stop_row):
                        field = board.fields[stop_column][stop_row]
                        if field.is_empty_or_is_opponent(piece.color):
                            final_piece = field.piece
                            stop = Field(stop_column, stop_row, final_piece)
                            move = Move(start, stop)
                            if check_verify:
                                if not AllowedMoves.under_check(piece, move, board):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            if field.is_opponent(piece.color):
                                break
                        else:
                            break
                    else:
                        break

        # ---------------------------- #
        piece.clear_moves()

        if isinstance(piece, Pawn):
            allowed_steps = 1 if piece.moved else 2

            # straight moves
            begin = row + piece.direction
            end = row + (piece.direction * (1 + allowed_steps))
            for possible_move in range(begin, end, piece.direction):
                if Field.in_range(possible_move):
                    if board.fields[column][possible_move].is_empty():
                        start = Field(column, row)
                        stop = Field(column, possible_move)
                        move = Move(start, stop)
                        if check_verify:
                            if not AllowedMoves.under_check(piece, move, board):
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
                    if board.fields[possible_move][possible_row].is_opponent(piece.color):
                        start = Field(column, row)
                        final_piece = board.fields[possible_move][possible_row].piece
                        stop = Field(possible_move, possible_row, final_piece)
                        move = Move(start, stop)
                        if check_verify:
                            if not AllowedMoves.under_check(piece, move, board):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

            # en passant
            r = 3 if piece.color == 'white' else 4
            final_row = 2 if piece.color == 'white' else 5
            for i in [-1, 1]:
                if Field.in_range(column - i) and row == r:
                    if board.fields[column - i][r].is_opponent(piece.color):
                        p = board.fields[column - i][row].piece
                        if isinstance(p, Pawn):
                            if p.en_passant:
                                start = Field(column, row)
                                stop = Field(column - i, final_row, p)
                                move = Move(start, stop)
                                if check_verify:
                                    if not AllowedMoves.under_check(piece, move, board):
                                        piece.add_move(move)
                                else:
                                    piece.add_move(move)

        elif isinstance(piece, Knight):
            around_moves(Knight.special_moves(column, row))
        elif isinstance(piece, Bishop):
            longitudinal_moves(Bishop.special_moves())
        elif isinstance(piece, Rook):
            longitudinal_moves(Rook.special_moves())
        elif isinstance(piece, Queen):
            longitudinal_moves(Queen.special_moves())
        elif isinstance(piece, King):
            around_moves(King.special_moves(column, row))
            # castling
            if not piece.moved:
                closer_rook = board.fields[7][row].piece
                further_rook = board.fields[0][row].piece
                if isinstance(further_rook, Rook) and not further_rook.moved:
                    # checking if is piece between Rook and King
                    # to add check method
                    for c in range(1, 4):
                        if board.fields[c][row].is_not_empty():
                            break
                        if c == 3:
                            piece.further_rook = further_rook

                            start = Field(0, row)
                            stop = Field(3, row)
                            move_rook = Move(start, stop)

                            start = Field(column, row)
                            stop = Field(2, row)
                            move_king = Move(start, stop)

                            if check_verify:
                                if AllowedMoves.under_check(piece, move_king, board, castling_check=True):
                                    if not AllowedMoves.under_check(piece, move_king, board)\
                                            and not AllowedMoves.under_check(further_rook, move_rook, board):
                                        piece.add_move(move_king)
                                        further_rook.add_move(move_rook)
                            else:
                                piece.add_move(move_king)
                                further_rook.add_move(move_rook)

                if isinstance(closer_rook, Rook) and not closer_rook.moved:
                    # checking if is piece between Rook and King
                    for c in range(5, 7):
                        if board.fields[c][row].is_not_empty():
                            break
                        if c == 6:
                            piece.closer_rook = closer_rook

                            start = Field(7, row)
                            stop = Field(5, row)
                            move_rook = Move(start, stop)

                            start = Field(column, row)
                            stop = Field(6, row)
                            move_king = Move(start, stop)

                            if check_verify:
                                if AllowedMoves.under_check(piece, move_king, board, castling_check=True):
                                    if not AllowedMoves.under_check(piece, move_king, board)\
                                            and not AllowedMoves.under_check(closer_rook, move_rook, board):
                                        piece.add_move(move_king)
                                        closer_rook.add_move(move_rook)
                            else:
                                piece.add_move(move_king)
                                closer_rook.add_move(move_rook)
        if boolean:
            if piece.moves:
                piece.clear_moves()
                return True
            else:
                return False

        # ---------------------------- #

    @staticmethod
    def under_check(piece, move, board, castling_check=False):
        def result():
            for column in range(COLUMNS):
                for row in range(ROWS):
                    if temp_board.fields[column][row].is_opponent(piece.color):
                        opponent = temp_board.fields[column][row].piece
                        AllowedMoves.detect(opponent, column, row, temp_board, check_verify=False)
                        for opponent_move in opponent.moves:
                            if isinstance(opponent_move.stop.piece, King):
                                return True
            return False

        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(board)
        if castling_check:
            if (move.start.column - move.stop.column) > 0:
                l_r, r_r = 2, 4
            else:
                l_r, r_r = 5, 7
            end_row = move.stop.row
            for i in range(l_r, r_r):
                temp_board.fields[i][end_row].piece = temp_piece
        else:
            temp_board.move(temp_piece, move, remover=True)

        if castling_check:
            return not result()
        else:
            return result()

    @staticmethod
    def check_promotion(piece, stop, board):
        if stop.row == 0 or stop.row == 7:
            board.fields[stop.column][stop.row].piece = Queen(piece.color)

    @staticmethod
    def en_passant_set(piece, board):
        if isinstance(piece, Pawn):
            for column in range(COLUMNS):
                for row in range(ROWS):
                    if isinstance(board.fields[column][row].piece, Pawn):
                        board.fields[column][row].piece.en_passant = False
            piece.en_passant = True

    @staticmethod
    def en_passant_capture_sound(piece, start, stop, board, remover):
        diff = stop.column - start.column
        if diff != 0 and board.fields[stop.column][stop.row].is_empty():
            board.fields[stop.column][start.row].piece = None
            board.fields[stop.column][stop.row].piece = piece
            if not remover:
                sound = Sound(os.path.join(
                    'sounds/capture.wav'
                ))
                sound.play()

    @staticmethod
    def castling(piece, start, stop, board, remover):
        if isinstance(piece, King):
            if abs(start.column - stop.column) == 2 and not remover:
                diff = stop.column - start.column
                rook = piece.further_rook if (diff < 0) else piece.closer_rook
                board.move(rook, rook.moves[-1])
