import pygame.transform

from code.const import WINDOW_WIDTH, WINDOW_HEIGHT
from code.entity import Entity

class Background(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.surf = pygame.transform.smoothscale(self.surf, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.rect = self.surf.get_rect(left = position [0], top = position[1])

    def move(self, ):
        self.rect.centerx -= 0
        if self.rect.right <= 0:
            self.rect.left = WINDOW_WIDTH
