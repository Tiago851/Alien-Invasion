#Important modules
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	#Class for a single alien

	def __init__(self, ai_game):

		#Initializing the game 
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings

		#Load alien image from folder
		self.image = pygame.image.load("alien.bmp")
		self.rect = self.image.get_rect()

		#Start a new alien on the top left corner of the screen
		#The dimensions of the alien ship are equal to the image dimensions
		self.rect.x = self.rect.width 
		self.rect.y = self.rect.height

		#Store the alien's horizontal position
		self.x = float(self.rect.x)

	def check_edges(self):
		#Return True if the ship is at the edge of the screen
		screen_edge = self.screen.get_rect()

		if self.rect.right >= screen_edge.right or self.rect.left <=0:
			return True

	def update(self):
		#Moving the ship to the right
		self.x += self.settings.alien_speed*self.settings.fleet_direction

		#Updating the x coordinates of the fleet
		self.rect.x = self.x 