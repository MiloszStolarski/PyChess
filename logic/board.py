from logic.const import ROWS, COLUMNS
from logic.field import Field
from logic.piece import *
from logic.allowed_moves import AllowedMoves
from menu.ending import Ending


class Board:

    def __init__(self):
        self.fields = [[Field(column, row) for row in range(ROWS)] for column in range(COLUMNS)]
        self.last_move = None
        #self._add_pieces('white')
        #self._add_pieces('black')
        self.ending = Ending(self)
        self.game_result = None
        self._test_board()

    def move(self, piece, move, remover=False):

        start = move.start
        stop = move.stop

        if isinstance(piece, Pawn):
            AllowedMoves.en_passant_capture_sound(piece, start, stop, self, remover)

        # board update
        self.fields[start.column][start.row].piece = None
        self.fields[stop.column][stop.row].piece = piece

        if isinstance(piece, Pawn):
            AllowedMoves.check_promotion(piece, stop, self)

        AllowedMoves.castling(piece, start, stop, self, remover)

        piece.moved = True
        piece.clear_moves()

        self.last_move = move

        self.game_result = self.ending.check_result(piece, self.last_move)

    @staticmethod
    def valid_move(piece, move):
        return move in piece.moves

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

        # add rooks
        self.fields[0][row_other].piece = Rook(color)
        self.fields[7][row_other].piece = Rook(color)

        # add queen
        self.fields[3][row_other].piece = Queen(color)

        # add king
        self.fields[4][row_other].piece = King(color)

    def _test_board(self):
        self.fields[7][0].piece = King('white')
        self.fields[0][5].piece = Rook('white')
        self.fields[0][4].piece = Rook('white')

        self.fields[5][1].piece = King('black')
        self.fields[4][4].piece = Knight('black')
