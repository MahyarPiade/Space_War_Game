import json
import os


class GameStats:
    """Track statics for Alien Invasion"""
    def __init__(self, sw_game):
        """Initialize statics"""
        self.settings = sw_game.setting
        self.reset_stats()
        self.game_active = False
        self._save_game()

    def reset_stats(self):
        """Initialize statics that can change throughout the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def _save_game(self):
        """Save the high score in a json file"""
        if not os.path.exists("high_score.json"):
            with open("high_score.json", "w") as high:
                json.dump(0, high)
            with open("high_score.json") as h:
                self.high_score = json.load(h)
        else:
            with open("high_score.json") as h:
                self.high_score = json.load(h)
