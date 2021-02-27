#Class to track game statistics

class GameStats:
	
	def __init__(self, ai_game):
		#Initialize statistics
		self.settings = ai_game.settings
		self.reset_stats()

		#Start Alien Invasion in an inactive state
		self.game_active = False

		#High score should never be reset
		f2 = open("high_score.txt","r")
		last_high_score = f2.readline()
		self.high_score = last_high_score
		f2.close()

		#The player's level
		self.level = 1

	def reset_stats(self):
		#Initialize statistics that change during the game
		self.ships_left = self.settings.ship_limit
		self.score = 0
