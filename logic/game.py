import pygame

from logic.const import *
from logic.board import Board
from logic.dragger import Dragger
from visual.config import Config
from logic.field import Field


class Game:

    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
        self.next_player = 'white'
        self.config = Config()

    def show_board(self, screen):
        theme = self.config.theme
        for row in range(ROWS):
            for column in range(COLUMNS):
                color = theme.chess_board.light if (row + column) % 2 else theme.chess_board.dark
                rect = (column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                pygame.draw.rect(screen, color, rect)

                if column == 0:
                    color = theme.chess_board.dark if row % 2 else theme.chess_board.light
                    label = self.config.font.render(str(ROWS - row), 1, color)
                    label_pos = (5, 5 + row * SQ_SIZE)
                    screen.blit(label, label_pos)

                if row == 7:
                    color = theme.chess_board.dark if (row + column) % 2 else theme.chess_board.light
                    label = self.config.font.render(Field.get_alphacol(column), 1, color)
                    label_pos = (column * SQ_SIZE + SQ_SIZE - 15, HEIGHT - 20)
                    screen.blit(label, label_pos)

    def show_pieces(self, screen):

        for row in range(ROWS):
            for column in range(COLUMNS):
                if not self.board.fields[column][row].is_empty():
                    piece = self.board.fields[column][row].piece

                    if piece is not self.dragger.dragged_piece:
                        piece.set_image(size=DEFAULT_SIZE)
                        image = pygame.image.load(piece.image_path)
                        image_center = column * SQ_SIZE + SQ_SIZE // 2, row * SQ_SIZE + SQ_SIZE // 2
                        piece.image_rect = image.get_rect(center=image_center)

                        screen.blit(image, piece.image_rect)

    def show_moves(self, screen):
        theme = self.config.theme
        if self.dragger.dragging:
            piece = self.dragger.dragged_piece

            for move in piece.moves:
                color = theme.moves.light if (move.stop.column + move.stop.row) % 2 else theme.moves.dark
                rect = (move.stop.column * SQ_SIZE + 1/12*SQ_SIZE, move.stop.row * SQ_SIZE + 1/12*SQ_SIZE,
                        5*SQ_SIZE/6, 5*SQ_SIZE/6)
                pygame.draw.rect(screen, color, rect, border_radius=7)

    def show_last_move(self, screen):
        theme = self.config.theme
        if self.board.last_move:
            start = self.board.last_move.start
            stop = self.board.last_move.stop

            for field in [start, stop]:
                color = theme.trace.light if (field.column + field.row) % 2 else theme.trace.dark
                rect = (field.column * SQ_SIZE + 1/24*SQ_SIZE, field.row * SQ_SIZE + 1/24*SQ_SIZE,
                        11*SQ_SIZE/12, 11*SQ_SIZE/12)
                pygame.draw.rect(screen, color, rect, border_radius=7)

    def change_theme(self):
        self.config.change_theme()

    def sound_effect(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'
