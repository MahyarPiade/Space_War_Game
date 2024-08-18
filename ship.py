import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """A class to manage the ship"""
    def __init__(self, ai_game):
        super().__init__()
        """Initialize the ship and set its starting position"""
        self.screen = ai_game.screen
        self.color_key = "white"
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect and make the rect invisible.
        self.image = pygame.image.load("Ship.jpeg")
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.image.set_colorkey(self.color_key)
        self.rect = self.image.get_rect()
        self.rect.clamp_ip(self.screen_rect)

        # start each new ship at bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Draw the ship at its current position"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def update(self):
        self.image = pygame.transform.scale(self.image, (50, 50))
