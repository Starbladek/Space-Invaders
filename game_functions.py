import sys
from time import sleep
import random
import pygame
from bullet import Bullet
from alien_laser import AlienLaser
from alien import Alien
from alien_explosion import AlienExplosion
from bunker import Bunker


def check_keydown_events(event, ai_settings, game_master, screen, ship, bullets):
    """Respond to keypresses"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, game_master, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, game_master, screen, ship, bullets):
    """Fire a bullet if limit not reached yet"""
    # Create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        game_master.ship_laser.play()


def update_bullets(ai_settings, game_master, screen, stats, sb, bunkers, aliens, bullets):
    """Update position of bullets and get rid of old bullets"""
    # Update bullet positions
    bullets.update()

    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, game_master, screen, stats, sb, aliens, bullets)
    check_bullet_bunker_collisions(bullets, bunkers)


def check_bullet_alien_collisions(ai_settings, game_master, screen, stats, sb, aliens, bullets):
    """Respond to bullet-alien collisions"""
    # Remove any bullets and aliens tai_settings, screen, ship, aliens, bullets that have collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            for alien in aliens:
                stats.score += alien.points
                alien_explosion = AlienExplosion(screen)
                alien_explosion.rect.center = alien.rect.center
                game_master.alien_explosions.append(alien_explosion)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, aliens)


def check_bullet_bunker_collisions(bullets, bunkers):
    pygame.sprite.groupcollide(bullets, bunkers, True, False)


def update_lasers(ai_settings, screen, game_master, aliens, lasers, ship, bunkers, stats, sb, bullets):
    if pygame.time.get_ticks() > game_master.next_laser_shot:
        game_master.last_laser_shot = game_master.next_laser_shot
        game_master.next_laser_shot = pygame.time.get_ticks() + random.randrange(250, 2000)
        temp = random.randrange(0, len(aliens))
        i = 0
        for alien in aliens:
            i += 1
            if i == temp:
                new_laser = AlienLaser(ai_settings, screen, alien)
                lasers.add(new_laser)
                game_master.alien_laser.play()

    lasers.update()
    for laser in lasers.copy():
        if laser.rect.top >= 800:
            lasers.remove(laser)

    check_laser_ship_collision(lasers, ship, stats, sb, bullets)
    check_bullet_bunker_collisions(lasers, bunkers)


def check_laser_ship_collision(lasers, ship, stats, sb, bullets):
    collision = pygame.sprite.spritecollideany(ship, lasers)
    if collision:
        sleep(0.5)
        if stats.ships_left > 0:
            stats.ships_left -= 1
            sb.prep_ships()
            bullets.empty()
            lasers.empty()
            ship.center_ship()
        else:
            stats.game_active = False
            pygame.mouse.set_visible(True)


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien"""
    if stats.ships_left > 0:
        # Decrement ships_left
        stats.ships_left -= 1

        # Update scoreboard
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_high_score(stats, sb):
    """Check to see if there's a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_keyup_events(event, ship):
    """Respond to key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(ai_settings, game_master, screen, stats, sb, play_btn, ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play"""
    button_clicked = play_btn.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, aliens)
        ship.center_ship()

        game_master.ufo = None
        game_master.next_ufo_spawn = pygame.time.get_ticks() + 10000


def check_events(ai_settings, gm, screen, stats, sb, play_button, ship, aliens, bullets):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, gm, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, gm, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def create_bunkers(bunkers, screen):
    for i in range(4):
        bunker = Bunker(screen)
        bunker.rect.x = 175 + (i * 250)
        bunker.rect.y = 600
        bunkers.add(bunker)


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row"""
    if row_number == 0:
        alien = Alien(ai_settings, screen, 1)
    elif row_number == 1 or row_number == 2:
        alien = Alien(ai_settings, screen, 2)
    else:
        alien = Alien(ai_settings, screen, 3)
    alien.x = 180 + (75 * alien_number)
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, aliens):
    """Create a full fleet of aliens"""
    number_aliens_x = 11
    number_rows = 5

    # Create the fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Check if the fleet is at an edge,
    and then update the positions of all aliens in the fleet"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)


def update_screen(ai_settings, screen, sb, ship, bunkers, aliens, alien_explosions, lasers, bullets, ufo):
    """Update images on the screen and flip to the new screen"""
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    for bunker in bunkers:
        bunker.blitme()

    for alien in aliens:
        alien.blitme()

    for alien_explosion in alien_explosions:
        alien_explosion.blitme()

    for laser in lasers.sprites():
        laser.draw_laser()

    if ufo:
        ufo.blitme()

    # Draw the score information
    sb.show_score()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_title_screen(play_button, title_screen):
    title_screen.blitme()
    play_button.draw_button()
    pygame.display.flip()
