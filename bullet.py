#Important modules
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""docstring for ClassName"""
	
	def __init__(self, ai_game):
		
		super().__init__() #Inheritance from Sprite
		
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.color = self.settings.bullet_color

		#Create a bullet rect at (0,0) and then correct the position
		self.rect = pygame.Rect(0,0,self.settings.bullet_width,
			self.settings.bullet_height)

		#Link the bullet to the ship's position. 
		#Midtop to make it look like he bullet comes out from the top of the ship
		self.rect.midtop = ai_game.ship.rect.midtop

		#Store the bullet's position 
		self.y = float(self.rect.y)

	def update(self):
		#Move the bullet upwards
		#Update its decimal position 
		self.y -= self.settings.bullet_speed

		#Update the rect position
		self.rect.y = self.y

	def draw_bullet(self):
		#Moving the bullet onto the screen
		pygame.draw.rect(self.screen,self.color,self.rect)