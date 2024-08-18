import pygame


class Bg:
    """Initializing a picture for background"""
    def __init__(self, ai_game):
        self.bg_image = pygame.image.load("space_2.jpg")
        self.bg_image = pygame.transform.scale(self.bg_image, (1280, 720))
        self.background_surface = pygame.Surface(ai_game.screen.get_size())
        self.background_surface.blit(self.bg_image, (0, 0))


