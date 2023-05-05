import pygame
from logic.game import Game
from menu.button import Button
from logic.field import Field
from logic.move import Move
from logic.const import *


class Main:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("PyChess")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game = Game()
        self.clock = pygame.time.Clock()

    def run(self):
        screen = self.screen
        game = self.game
        dragger = self.game.dragger
        board = self.game.board

        while True:
            game.show_board(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            if dragger.dragging:
                dragger.piece_dragging(screen)

            # --- Process player inputs ---
            for event in pygame.event.get():
                # Click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("#--------------------------------------------------------#")
                    dragger.update_mouse(event.pos)

                    clicked_column = dragger.mouse_coords[0] // SQ_SIZE
                    clicked_row = dragger.mouse_coords[1] // SQ_SIZE

                    if clicked_column < COLUMNS and clicked_row < ROWS:
                        print(board.fields[clicked_column][clicked_row].piece)

                        if board.fields[clicked_column][clicked_row].is_not_empty():
                            piece = board.fields[clicked_column][clicked_row].piece
                            if piece.color == game.next_player:
                                board.allowed_moves(piece, clicked_column, clicked_row)
                                dragger.save_coords((clicked_column, clicked_row))
                                dragger.drag_piece(piece)
                                game.show_board(screen)
                                game.show_last_move(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen)

                # Mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_board(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        dragger.piece_dragging(screen)

                # Click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_column = dragger.mouse_coords[0] // SQ_SIZE
                        released_row = dragger.mouse_coords[1] // SQ_SIZE

                        start = Field(dragger.initial_coords[0], dragger.initial_coords[1])
                        stop = Field(released_column, released_row)
                        move = Move(start, stop)

                        if board.valid_move(dragger.dragged_piece, move):
                            captured = board.fields[released_column][released_row].is_not_empty()
                            board.move(dragger.dragged_piece, move)
                            board.en_passant_set(dragger.dragged_piece)
                            game.sound_effect(captured)
                            game.show_board(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            game.next_turn()

                    dragger.undrag_piece()

                # Keyboard
                elif event.type == pygame.KEYDOWN:
                    # change theme
                    if event.key == pygame.K_c:
                        game.change_theme()

                # Cross for the window
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
            """
            # Logical updates
            for obj in self.objects:
                obj.process(self.screen)
            """
            self.clock.tick(FPS)
            pygame.display.update()


main = Main()
main.run()
