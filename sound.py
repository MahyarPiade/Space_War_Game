import pygame
import pygame.mixer


class Sound:
    """Initialize the sound effect and background music of the game"""
    def __init__(self):
        self.bg_music = pygame.mixer.music.load("bg_music.mp3")
        pygame.mixer.music.set_volume(1)

        self.bullet_sound = pygame.mixer.Sound("bullet_sound_1.wav")
        self.bullet_sound.set_volume(0.25)

    def fire_sound(self):
        self.bullet_sound.play()

    def bg_sound(self):
        pygame.mixer.music.play(-1)
