import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien"""
    def __init__(self, sw_game):
        """Initialize the alien and set its starting position"""
        super().__init__()
        self.screen = sw_game.screen
        self.setting = sw_game.setting
        self.image_color_key = "white"

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load("alien_ship_3.jpeg")
        self.image = pygame.transform.scale(self.image, (65, 65))
        self.image.set_colorkey(self.image_color_key)
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # self.rect.topleft

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def update(self):
        """Move the alien right or left"""
        self.x += (self.setting.alien_speed * self.setting.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return True if an alien is the edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
