import pygame
from pygame.sprite import Sprite


class TitleScreen(Sprite):
    def __init__(self, screen):
        super(TitleScreen, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('images/title_screen.png')
        self.rect = self.image.get_rect()

    def blitme(self):
        self.screen.blit(self.image, self.rect)
