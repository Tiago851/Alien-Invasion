#Settings of the game. This class is also useful to don't hardcode the settings
from win32api import GetSystemMetrics

class Settings:
	#Class to store the settings of the game

	def __init__(self):
		#Screen settings
		self.screen_width = GetSystemMetrics(0)
		self.screen_height = GetSystemMetrics(1)
		self.bg_color = (230,230,230)

		#Adjusting the ship's speed
		self.ship_speed = 1.5
		self.ship_limit = 3

		#Drawing the bullets and their settings
		self.bullet_speed = 1.0
		self.bullet_width = 300
		self.bullet_height = 15
		self.bullet_color = (60,60,60)
		self.bullets_allowed = 3 #Limiting the number of bullets onscreen

		#Alien settings
		self.alien_speed = 0.5
		self.fleet_drop_speed = 10

		# fleet_direction > 0 the aliens move to the right
		self.fleet_direction = 1

		#How quickly the game speeds up
		self.speedup_scale = 1.1

		#How quickly the alien point values increase
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		#Initialize the settings that change throughout the game
		self.ship_speed = 1.5
		self.bullet_speed = 3.0
		self.alien_speed = 1.0

		#Fleet direction 
		self.fleet_direction = 1

		#Scoring
		self.alien_points = 50

	def increase_speed(self):
		#Increase speed settings
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale

		self.alien_points = int(self.alien_points*self.score_scale)
