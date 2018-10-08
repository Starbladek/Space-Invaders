import pygame
from pygame.sprite import Sprite


class Bunker(Sprite):

    def __init__(self, screen):
        """Initialize the ship and set its starting position"""
        super(Bunker, self).__init__()
        self.screen = screen

        # Load the ship image and get its rect
        self.image = pygame.image.load('images/bunker.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
