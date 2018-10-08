import pygame
import random
from ufo import UFO
import game_functions as gf


class GameMaster:
    def __init__(self, screen):
        self.screen = screen
        self.last_laser_shot = 0
        self.next_laser_shot = 0
        self.last_ufo_spawn = 0
        self.next_ufo_spawn = 0
        self.ufo = None
        self.alien_explosions = []
        self.ship_laser = pygame.mixer.Sound('sounds/ship_laser.wav')
        self.alien_laser = pygame.mixer.Sound('sounds/alien_laser.wav')

    def check_ufo_spawn(self, screen, bullets, stats, sb):
        for alien_explosion in self.alien_explosions:
            alien_explosion.update()
            if alien_explosion.frame_counter > 10:
                self.alien_explosions.remove(alien_explosion)
        if self.ufo:
            self.ufo.update()
            if self.ufo.rect.right < self.screen.get_rect().left:
                self.ufo = None
            else:
                self.check_bullet_ufo_collision(bullets, stats, sb)
        if pygame.time.get_ticks() > self.next_ufo_spawn:
            self.last_ufo_spawn = self.next_ufo_spawn
            self.next_ufo_spawn = pygame.time.get_ticks() + random.randrange(10000, 20000)
            self.ufo = UFO(screen)

    def check_bullet_ufo_collision(self, bullets, stats, sb):
            collision = pygame.sprite.spritecollide(self.ufo, bullets, True)
            if collision:
                self.ufo = None
                stats.score += 100
                sb.prep_score()
                gf.check_high_score(stats, sb)
