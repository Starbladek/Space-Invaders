import pygame
from pygame.sprite import Sprite


class AlienExplosion(Sprite):
    def __init__(self, screen):
        super(AlienExplosion, self).__init__()
        self.screen = screen

        self.image1 = pygame.image.load('images/alien_explode1.png')
        self.image2 = pygame.image.load('images/alien_explode2.png')
        self.image3 = pygame.image.load('images/alien_explode3.png')
        self.current_image = self.image1
        self.rect = self.current_image.get_rect()

        self.next_frame = pygame.time.get_ticks() + 50
        self.frame_counter = 0

        self.alien_explosion = pygame.mixer.Sound('sounds/alien_explosion.wav')
        self.alien_explosion.play()

    def update(self):
        if pygame.time.get_ticks() > self.next_frame:
            self.next_frame = pygame.time.get_ticks() + 50
            self.frame_counter += 1
            if self.current_image == self.image1:
                self.current_image = self.image2
            elif self.current_image == self.image2:
                self.current_image = self.image3
            else:
                self.current_image = self.image1

    def blitme(self):
        self.screen.blit(self.current_image, self.rect)
