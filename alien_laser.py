import pygame
from pygame.sprite import Sprite


class AlienLaser(Sprite):

    def __init__(self, ai_settings, screen, alien):
        """Create a laser object at the alien's current position"""
        super(AlienLaser, self).__init__()
        self.screen = screen

        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom

        self.y = float(self.rect.y)

        self.color = ai_settings.laser_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Move the laser down the screen"""
        # Update the decimal position of the bullet
        self.y += self.speed_factor
        # Update the rect position
        self.rect.y = self.y

    def draw_laser(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
