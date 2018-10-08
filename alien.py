import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, ai_settings, screen, alien_type):
        """Initialize the alien and set its starting position"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image and set its rect attribute
        if alien_type == 1:
            self.image = pygame.image.load('images/squid_alien1.png')
            self.image2 = pygame.image.load('images/squid_alien2.png')
            self.points = ai_settings.squid_alien_points
        elif alien_type == 2:
            self.image = pygame.image.load('images/crab_alien1.png')
            self.image2 = pygame.image.load('images/crab_alien2.png')
            self.points = ai_settings.crab_alien_points
        elif alien_type == 3:
            self.image = pygame.image.load('images/skull_alien1.png')
            self.image2 = pygame.image.load('images/skull_alien2.png')
            self.points = ai_settings.skull_alien_points

        self.current_image = self.image
        self.rect = self.current_image.get_rect()

        self.next_animation_frame = pygame.time.get_ticks() + 100

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen"""
        if pygame.time.get_ticks() > self.next_animation_frame:
            self.next_animation_frame = pygame.time.get_ticks() + 100
            if self.current_image == self.image:
                self.current_image = self.image2
            else:
                self.current_image = self.image

        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right or left"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        """Draw the alien at its current location"""
        self.screen.blit(self.current_image, self.rect)
