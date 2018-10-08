import pygame
import random
from pygame.sprite import Group
from settings import Settings
from game_master import GameMaster
from title_screen import TitleScreen
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf


def run_game():
    # Initialize pygame, settings, and screen object
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    game_master = GameMaster(screen)
    title_screen = TitleScreen(screen)
    pygame.display.set_caption("Space Invaders")

    # Make the Play button
    play_button = Button(screen, "Play")

    # Create an instance to store game statistics and create a scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make a ship, group of bunkers, a group of bullets, and a group of aliens
    ship = Ship(ai_settings, screen)
    bunkers = Group()
    bullets = Group()
    aliens = Group()
    lasers = Group()

    game_master.last_laser_shot = pygame.time.get_ticks()
    game_master.next_laser_shot = game_master.last_laser_shot + random.randrange(250, 2000)

    gf.create_bunkers(bunkers, screen)
    gf.create_fleet(ai_settings, screen, aliens)

    # Start the main loop for the game
    while True:
        gf.check_events(ai_settings, game_master, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, game_master, screen, stats, sb, bunkers, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)
            gf.update_lasers(ai_settings, screen, game_master, aliens, lasers, ship, bunkers, stats, sb, bullets)
            gf.update_screen(ai_settings, screen, sb, ship, bunkers, aliens, game_master.alien_explosions,
                             lasers, bullets, game_master.ufo)
            game_master.check_ufo_spawn(screen, bullets, stats, sb)
        else:
            gf.update_title_screen(play_button, title_screen)


run_game()
