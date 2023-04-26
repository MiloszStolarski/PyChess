import pygame
from logic.const import *


class Button:

    def __init__(self, screen, x, y, width, height, button_text='Button', function=None):
        self.x = x - width/2
        self.y = y - height/2
        self.width = width
        self.height = height
        self.function = function
        self.screen = screen

        self.fillColors = {
            'normal': 'green',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.button_surface = pygame.Surface((self.width, self.height))
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        font = pygame.font.SysFont(FONT_TITLE, FONT_SIZE)
        self.button_surf = font.render(button_text, True, 'white')

    def process(self, screen):
        mouse_pos = pygame.mouse.get_pos()  # fps check!
        self.button_surface.fill(self.fillColors['normal'])
        if self.button_rect.collidepoint(mouse_pos):
            self.button_surface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface.fill(self.fillColors['pressed'])
                self.function()
        self.button_surface.blit(self.button_surf, [
            self.button_rect.width / 2 - self.button_surf.get_rect().width / 2,
            self.button_rect.height / 2 - self.button_surf.get_rect().height / 2
        ])
        screen.blit(self.button_surface, self.button_rect)
