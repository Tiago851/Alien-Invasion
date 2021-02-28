#Main class for the game

#Important modules
import sys
import pygame
from settings import *
from ship import *
from bullet import *
from alien import *
from time import sleep
from game_stats import GameStats
from button import *
from scoreboard import *

class AlienInvasion:
	"""Class to manage the game"""

	def __init__(self):
		
		pygame.init()
		self.settings = Settings()

		#Defining the dimensions of the game window - Full Screen / pretty cool stuff ;) 
		self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height

		#Title of the window
		pygame.display.set_caption("Alien Invasion")

		#Creating an instance to score game statistics and a scoreboard
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		#Entering the ship in the main game
		self.ship = Ship(self) #aqui é preciso por o self para o ship ter acesso aos recursos do jogo

		#Group to manage the bullets already fired
		self.bullets = pygame.sprite.Group()

		#Group to handle the alien ships
		self.aliens = pygame.sprite.Group()

		#Method for the alien fleet
		self._create_fleet()

		#Adding the button
		self.play_button = Button(self,"Click here to play or Press P")

		#Background color
		self.bg_color = (230,230,230)

	def run_game(self):
		#Main loop of the game

		while True:
			#This is the event manager.
			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()
			
			self._update_screen()

	def _check_events(self):
		#Responding to Keyboard and mouse movements
		for event in pygame.event.get():

			#Events triggered by pressing on the keyboard
			if event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)

			#Events triggered by releasing a key on the keyboard
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)

			#Quit the game by pressing X on the top right corner
			elif event.type == pygame.QUIT:
				self._quit_game()
				sys.exit()

			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_play_button(self,mouse_pos):
		#Start a new game when the player clicks Play

		button_clicked = self.play_button.rect.collidepoint(mouse_pos)

		if button_clicked and not self.stats.game_active:
			self.settings.initialize_dynamic_settings()
			self._start_game()


			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()

			#Reset the game statistics
			self.stats.reset_stats()
				
	def _check_keydown_events(self,event):
		#Refactor of the check_keydown events
		if event.key == pygame.K_RIGHT:
		#Move the ship to the right
			self.ship.moving_right = True

		#Move the ship to the left
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True

		#Quit the game by pressing Q on the keyboard
		elif event.key == pygame.K_q:
			self._quit_game()
			sys.exit()

		#Fire a bullet when Spacebar is pressed
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()

		elif event.key == pygame.K_p:
			self._start_game()


	def _quit_game(self):
		#Storing the High Score in a file
		f = open("high_score.txt","w+")
		f.write(str(self.stats.high_score))
		f.close()

	def _start_game(self):
		#Method for starting the game in 2 different ways

		#Resetting the game
		self.stats.reset_stats()

		#Activate the game after pressing Play
		self.stats.game_active = True

		#Get rid of any remaining aliens and bullets
		self.aliens.empty()
		self.bullets.empty()	

		#Create a new fleet and center the ship
		self._create_fleet()
		self.ship.center_ship()

		#Hide the mouse cursor
		pygame.mouse.set_visible(False)

	def _check_keyup_events(self,event):
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False

		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _fire_bullet(self):

		#Here we make sure that no more than the nr of allowed bullets are created and on the screen
		if len(self.bullets) < self.settings.bullets_allowed:
			#Create a new bullet and add it to the screen
			new_bullet = Bullet(self)
			#The add method here is similar to append, but specific for Pygames
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		#Updating the position of the bullets and get rid of old bullets
		self.bullets.update()

		#Delete the bullets after they reached the top of the screen
		#We use the copy() method here because it is not possible to loop through dynamic lists
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		
		self._check_bullet_alien_collisions()

	def _check_bullet_alien_collisions(self):
		#Responding to bullet-alien collisions

		#Remove any bullets and aliens
		collisions = pygame.sprite.groupcollide(
			self.bullets,self.aliens,False,True)

		if collisions:

			#Msking sure that each allien hit counts for the score 
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			
			self.sb.prep_score()

			#Each time an alien is hit, check and compare the high score
			self.sb.check_high_score()

		#If the fleet is destroyed, activate this option to create a whole new one
		if not self.aliens:
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

			#Increase level
			self.stats.level += 1
			self.sb.prep_level()

	def _create_fleet(self):
		#Creating a new fleet of aliens

		#Crearing an alien to know the spacing between aliens
		alien = Alien(self)
		alien_width,alien_height = alien.rect.size

		#Available space between aliens and max number of them in one row
		available_space_x = self.settings.screen_width - (2*alien_width)
		number_of_aliens = available_space_x // (2* alien_width)

		#Determine the number of rows of aliens fitting the screen
		ship_height = self.ship.rect.height
		available_space_y = self.settings.screen_height - (3*alien_height)-ship_height
		number_rows = available_space_y // (2*alien_height)

		#Create the full fleet of aliens
		for row_number in range(number_rows):
			for alien_number in range(number_of_aliens):
				self._create_alien(alien_number,row_number)

	def _create_alien(self,alien_number,row_number):
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2*alien_width*alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height+2*alien.rect.height*row_number
		self.aliens.add(alien)

	def _update_aliens(self):
		self._check_fleet_edges()
		self.aliens.update()

		#Check if the ship and fleet collided
		if pygame.sprite.spritecollideany(self.ship,self.aliens):
			self._ship_hit()

		#Look for aliens hitting the bottom of the screen
		self._check_aliens_bottom()

	def _check_aliens_bottom(self):
		#Check if any aliens have reached the bottom of the screen

		screen_rect = self.screen.get_rect()

		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				#The same thing as if the ship is hit
				self._ship_hit()
				break

	def _ship_hit(self):
		#Response when the shit collides with an allien
		
		self._quit_game()
		
		if self.stats.ships_left > 0:
			#Decrement ships left
			self.stats.ships_left -= 1

			#The gamer loses a life/ship so the prep_ship needs to be called
			#Update the scoreboard
			self.sb.prep_ships()

			#Get rid of any remaining aliens and bullets
			self.aliens.empty()
			self.bullets.empty()

			#Create a new fleet and center the ship
			self._create_fleet()
			self.ship.center_ship()

			#Pause
			sleep(0.5)

		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

	def _check_fleet_edges(self):
		#Response if any of the aliens reached an edge
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		#Drop the fleet and change its direction
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed

		self.settings.fleet_direction *= -1 


	def _update_screen(self):
		#Redraw the screen after each event
		#Ter em atenção a ordem em que se coloca estes parametros!!!
		self.screen.fill(self.settings.bg_color)

		#Include the ship
		self.ship.blitme()

		#Returns a list of all sprites in the group bullets
		for bala in self.bullets.sprites():
			bala.draw_bullet()

		#Display the alien fleet
		self.aliens.draw(self.screen)

		#Draw the score information
		self.sb.show_score()

		#Draw the play button
		if not self.stats.game_active:
			self.play_button.draw_button()

		#Make the most recently drawn screen 
		pygame.display.flip()


if __name__ == '__main__':
	#Make the game instance and run it
	ai = AlienInvasion()
	ai.run_game()
