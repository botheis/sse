import pygame
from sse.obj import Obj

class Renderer:

    # To define in children class
    def display(self, entity:Obj, screen:pygame.surface.Surface):
        """TO BE DEFINED BY CHILDREN. This method is called to render the entity object in the screen.

        Args:
            self (Renderer): Instance of Renderer object.
            entity (sse.obj.Obj): The object to render in the screen.
            screen (pygame.surface.Surface): The engine.window surface.
        """
        pass

    def draw_rect(self, screen:pygame.surface.Surface, color, pos):
        """Fill the rect specified in pos with the specified color.

        Args:
            self (Renderer): Instance of Renderer object.
            screen (pygame.surface.Surface): The engine.window surface.
            color (tuple): (r, g, b) where r,g,b are between 0 and 255.
            pos (tuple): (x, y, w, h) where x and y are the starting point. w is the width and h is the height."""
        pygame.draw.rect(screen, color, pos)

    def fill(self, screen:pygame.surface.Surface, color):
        """Fill the screen with the color.

        Args:
            self (Renderer): Instance of Renderer object.
            color (tuple): (r, g, b) where r, g, b are between 0 and 255.
        """
        screen.fill(color)

    def blit(self, screen:pygame.surface.Surface, image:pygame.surface.Surface, pos, crop=None):
        """Blit an image on screen.

        Args:
            self (Renderer): Instance of Renderer object.
            screen (pygame.surface.Surface): the engine.window surface.
            image: (pygame.surface.SUrface): the image/texture to blit on screen.
            pos (tuple): (x, y, w, h) x,y are the position where the image has to be blitted. w(idth),h(eight) are the image dimension.
            crop (tuple, default=None): If defined as (x, y, w, h), uses the parameters to render partially the image (under the crop limits).
            """
        screen.blit(image, pos, crop)

    def print(self, screen:pygame.surface.Surface, text:str, font:pygame.font.Font, bg_color, fg_color, pos):
        """Print text using the specified font and colors.

        Args:
            self (Renderer): Instance of Renderer object.
            scren (pygame.surface.Surface): the engine.window screen.
            text (str): the text we whant to display on screen.
            font (pygame.font.Font): The font to use to render the text.
            bg_color (tuple): (r, g, b) where r, g, b are between 0 and 255.
            fg_color (tuple): (r, g, b) where r, g, b are between 0 and 255.
            pos (tuple): (x, y, w, h): the position of the texte on the screen."""
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

