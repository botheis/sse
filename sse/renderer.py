import pygame
from sse.obj import Obj

class Renderer:

    # To define in children class
    def display(self, entity:Obj, screen:pygame.surface.Surface):
        pass

    def draw_rect(self, screen:pygame.surface.Surface, color, pos):
        pygame.draw.rect(screen, color, pos)

    def fill(self, screen:pygame.surface.Surface, color):
        screen.fill(color)

    def blit(self, screen:pygame.surface.Surface, image:pygame.surface.Surface, pos, crop):
        screen.blit(image, pos, crop)

    def print(self, screen:pygame.surface.Surface, text:str, font:pygame.font.Font, bg_color, fg_color, pos):
        srf = font.render(text, True, fg_color, bg_color)
        size = srf.get_size()

        x = pos[0]
        y = pos[1]
        w = pos[2]
        h = pos[3]

        w1 = size[0]
        h1 = size[1]

        x1 = x + (w1 - w) / 2
        y1 = y + (h - h1) / 2

        pos1 = (x1, y1, w1, h1)
        self.blit(screen, srf, pos1, None)

