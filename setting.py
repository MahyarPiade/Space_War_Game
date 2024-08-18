class Settings:
    """A class to store all settings for Alien Invasion"""
    def __init__(self):
        """Initialize the game's static settings"""
        # screen setting:
        self.screen_width = 1280
        self.screen_height = 720

        # Ship setting:
        self.ship_limit = 3

        # Alien setting:
        self.fleet_drop_speed = 10

        # Bullet setting:
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullets_allowed = 1
        self.bullet_color = "grey"

        # Game speed_up scale:
        self.speed_up_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize the settings that change throughout the game"""
        self.ship_speed = 1.0
        self.bullet_speed = 2.0
        self.alien_speed = 1.0

        # fleet direction of 1 represents right; -1 represent left.
        self.fleet_direction = 1.0

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed setting"""
        self.ship_speed *= self.speed_up_scale
        self.bullet_speed *= self.speed_up_scale
        self.alien_speed *= self.speed_up_scale













