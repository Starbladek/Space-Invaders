import pygame
from pygame.sprite import Sprite


class UFO(Sprite):
    def __init__(self, screen):
        super(UFO, self).__init__()
        self.screen = screen

        self.image = pygame.image.load('images/ufo_alien.png')
        self.rect = self.image.get_rect()

        self.rect.left = 1200
        self.rect.centery = 100

        self.x = float(self.rect.x)

        self.ufo_hover_sound = pygame.mixer.Sound('sounds/ufo_hover.wav')
        self.next_hover_sound_play = pygame.time.get_ticks() + 150

    def update(self):
        if pygame.time.get_ticks() > self.next_hover_sound_play:
            self.ufo_hover_sound.play()
            self.next_hover_sound_play = pygame.time.get_ticks() + 150
        self.x -= 2
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)
