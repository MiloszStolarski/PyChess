import pygame
import os

from visual.sound import Sound
from visual.theme import Theme


class Config:

    def __init__(self):
        self.themes = []
        self._add_themes()
        self.idx = 0
        self.theme = self.themes[self.idx]
        self.font = pygame.font.SysFont('monospace', 18, bold=True)

        self.move_sound = Sound(
            os.path.join('sounds/move.wav')
        )
        self.capture_sound = Sound(
            os.path.join('sounds/capture.wav')
        )

    def change_theme(self):
        self.idx += 1
        self.idx %= len(self.themes)
        self.theme = self.themes[self.idx]

    def _add_themes(self):
        green = Theme((119, 154, 88), (234, 235, 200), (150, 190, 255), (150, 190, 255), (200, 200, 51), (200, 200, 51))
        classic = Theme((255, 206, 158), (209, 139, 71),  (128, 128, 128),  (128, 128, 128), (255, 255, 204), (122, 52, 0))
        pastel = Theme((240, 219, 180), (206, 145, 120),  (211, 211, 211),  (211, 211, 211), (181, 89, 37), (250, 231, 181))
        contrast = Theme((255, 255, 255), (50, 50, 50), (200, 200, 200), (200, 200, 200), (255, 140, 0), (255, 255, 102))
        class_m = Theme((255, 221, 181), (166, 96, 42), (128, 128, 128), (128, 128, 128), (128, 0, 0), (255, 255, 204))
        grey_white = Theme((245, 245, 245), (105, 105, 105), (128, 128, 128), (128, 128, 128), (0, 0, 128), (255, 255, 224))
        nature = Theme((245, 222, 179), (141, 110, 99), (128, 128, 128), (128, 128, 128), (94, 38, 18), (255, 228, 181))
        white_black = Theme((255, 255, 255), (0, 0, 0), (128, 128, 128), (128, 128, 128), (255, 255, 255), (0, 0, 0))
        sapphire = Theme((218, 235, 253), (108, 142, 191), (128, 128, 128), (128, 128, 128), (255, 255, 204), (38, 76, 123))
        rustic = Theme((255, 215, 179), (165, 42, 42), (128, 128, 128), (128, 128, 128), (255, 255, 224), (139, 69, 19))
        grey_pink = Theme((245, 245, 245), (211, 211, 211), (128, 128, 128), (128, 128, 128), (238, 130, 238), (128, 0, 0))
        snow = Theme((245, 245, 245), (119, 136, 153), (128, 128, 128), (128, 128, 128), (240, 248, 255), (25, 25, 112))

        self.themes = [green, classic, pastel, contrast, class_m,
                       grey_white, nature, white_black, sapphire,
                       rustic, grey_pink, snow]
