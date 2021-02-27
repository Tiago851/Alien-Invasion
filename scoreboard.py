#Class to display the scoring information

#Important modules
from pygame.sprite import Group
import pygame.font
from ship import *

class Scoreboard:

	def __init__(self,ai_game):

		self.ai_game = ai_game
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = ai_game.settings
		self.stats = ai_game.stats

		#Font settings for scoring information
		self.text_color = (30,30,30)
		self.font = pygame.font.SysFont(None,48)

		#Prepare the initial score image
		self.prep_score()

		#The high score is displayed seperately from the score
		self.prep_high_score()

		#Display the level
		self.prep_level()

		#Import the group of ships and Ship classes
		self.prep_ships()

	def prep_score(self):
		#Turn the score into a rendered image

		#Turn the score into a multiple of 10 with commas
		rounded_score = round(self.stats.score, -1)
		score_str = "{:,}".format(rounded_score)

		self.score_image = self.font.render(score_str,True,
			self.text_color, self.settings.bg_color)

		#Display the score at the top right of the screen
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20


	def check_high_score(self):
		#Check for a new high score
		if self.stats.score > int(self.stats.high_score):
			self.stats.high_score = self.stats.score
			self.prep_high_score()

	def prep_high_score(self):
		#Turn the high score into a rendered image
		high_score = round(int(self.stats.high_score),-1)
		high_score_str = "{:,}".format(high_score)

		self.high_score_image = self.font.render("Highest Score: "+high_score_str,True,
			self.text_color, self.settings.bg_color)

		#Display the score at the top right of the screen
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top

	def prep_level(self):
		#Turning the level into an image
		level_str = str(self.stats.level)

		self.level_image = self.font.render("Level: "+level_str,True,
			self.text_color, self.settings.bg_color)

		#Display the level at the top left of the corner
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.screen_rect.right
		self.level_rect.top = self.score_rect.bottom+10


	def prep_ships(self):
		#Show how many ships are left

		#Creating an empty group and hold the ship instances in it
		self.ships = Group()

		#Loop for every ship the player has left
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_game)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)

	def show_score(self):
		#Draw the score to the screen
		self.screen.blit(self.score_image,self.score_rect)
		self.screen.blit(self.high_score_image,self.high_score_rect)
		self.screen.blit(self.level_image,self.level_rect)
		self.ships.draw(self.screen)
