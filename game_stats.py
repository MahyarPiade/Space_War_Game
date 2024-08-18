class GameStats:
    """Track statics for Alien Invasion"""
    def __init__(self, ai_game):
        """Initialize statics"""
        self.settings = ai_game.setting
        self.reset_stats()
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        """Initialize statics that can change throughout the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1



