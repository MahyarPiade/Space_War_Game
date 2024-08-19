import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class for the bullets that are fired from the ship"""
    def __init__(self, sw_game):
        super().__init__()
        self.screen = sw_game.screen
        self.setting = sw_game.setting
        self.color = self.setting.bullet_color

        # create a bullet rect at (0, 0) and then set the correct position.
        self.rect = pygame.Rect(0, 0, self.setting.bullet_width, self.setting.bullet_height)
        self.rect.midtop = sw_game.ship.rect.midtop

        # store the bullet's position at a decimal value.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen"""

        # update the decimal position of the bullet.
        self.y -= self.setting.bullet_speed

        # update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)


