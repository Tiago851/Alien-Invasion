#Important modules
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

	def __init__(self,ai_game):

		#Make Ship inherit from Sprite to create a group of ships (?)
		super().__init__()

		#Setting up the ship and set the starting position
		self.screen = ai_game.screen
		self.screen_rect = ai_game.screen.get_rect()
		self.settings = ai_game.settings

		#Load the ship image
		self.image = pygame.image.load("ship.bmp")
		self.rect = self.image.get_rect()

		#Start each new ship in the bottom center of the screen
		self.rect.midbottom = self.screen_rect.midbottom

		#Store a decimal value for the ship's horizontal position
		self.x = float(self.rect.x)

		#Movement flag
		self.moving_right = False
		self.moving_left = False

	def blitme(self):
		#Draw the ship at its current location and onto the screen
		self.screen.blit(self.image,self.rect)


	def update(self):
		#Update the ship's position
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.ship_speed

		#Here it's better to use an independent if block instead of elif
		#in case of elif the movement to the right will have priority
		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings.ship_speed

		#Update rect object from self.x
		self.rect.x = self.x


	def center_ship(self):
		#Center the ship on the screen
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)
