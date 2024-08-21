import pygame
import sys
from setting import Settings
from ship import Ship
from bullet import Bullet
from bg import Bg
from alien import Alien
from game_stats import GameStats
from button import Button
from sound import Sound
from scoreboard import Scoreboard
from time import sleep


class SpaceWar:
    """Overall class to manage assets and behavior"""
    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        pygame.display.set_caption("Space Wars")
        self.run = True
        self.setting = Settings()
        self.screen = pygame.display.set_mode((self.setting.screen_width, self.setting.screen_height))
        self.sound = Sound()
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.back = Bg(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "Play")

    def key_detection(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self.ship.rect.left < 0:
                self.ship.rect.left = 0
            else:
                self.ship.rect.move_ip(-self.setting.ship_speed, 0)

        if keys[pygame.K_d]:
            if self.ship.rect.right > 1280:
                self.ship.rect.right = 1280
            else:
                self.ship.rect.move_ip(self.setting.ship_speed, 0)

        if keys[pygame.K_q]:
            sys.exit()

        if keys[pygame.K_SPACE]:
            self._fire_bullet()

    def _fire_bullet(self):
        """Create a new bullet and add it to the group"""
        if len(self.bullets) < self.setting.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.sound.fire_sound()

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond correctly if an alien hit the edges"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.setting.fleet_drop_speed
        self.setting.fleet_direction *= -1

    def _create_fleet(self):
        """Create fleet of aliens"""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.setting.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Create the full fleet of aliens.
        for row_number in range(3):
            # Create the first row of aliens.
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _check_bullet_alien_collision(self):
        # Check for any bullets that have hit aliens.
        # And as the result getting rid of both bullet and alien.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.setting.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.setting.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 1:
            # Decrement ships_left and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Get rid of the remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_alien_bottom(self):
        """Check if any alien have reached the bottom of screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Doing the same thing as if ship being hit by alien
                self._ship_hit()
                break

    def _update_alien(self):
        """Check if the fleet is at edge then update the position of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien_ship collision.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of screen.
        self._check_alien_bottom()

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        self.bullets.update()

        # Get rid of old bullets.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()

    def _update_screen(self):
        """Draw the elements of the game on the screen"""
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()
            self.sound.bg_sound()

    def _check_events(self):
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Starts a new game when the player hit the play button"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.setting.initialize_dynamic_settings()

            # Reset the game statics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of the remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def run_game(self):
        """Start the main loop for the game"""
        while self.run:
            self._check_events()
            if self.stats.game_active:
                self.key_detection()
                self.screen.blit(self.back.background_surface, (0, 0))
                self._update_bullets()
                self._update_alien()
            self._update_screen()

            # Make the most recently drawn screen visible.
            pygame.display.flip()


ai = SpaceWar()
ai.run_game()





