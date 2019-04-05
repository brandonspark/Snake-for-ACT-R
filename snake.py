from pygame.locals import *
import pygame
import time
import random

def isCollision(x1, y1, x2, y2):
	if (x1 == x2) and (y1 == y2):
		return True
	return False

def hitSelf(x1, y1, positions):
	for pos in positions:
		if (x1, y1) == pos:
			return True
	return False

def outOfBounds(x1, y1, width, height):
	if x1 > width or y1 > height or x1 < 0 or y1 < 0:
		return True
	return False

def appleInit(snek, rows, cols):
	x = random.randint(0, cols)
	y = random.randint(0, rows)
	while (x, y) in snek.positions:
		x = random.randint(0, cols)
		y = random.randint(0, rows)
	return (x, y)
	
class Snake:

	def __init__(self, length, direction, position):
		self.length = length + 20
		self.positions = [position] * self.length
		self.direction = direction
		self.curPos = self.positions[0]
	
	def moveRight(self):
		if not self.direction == "WEST":
			self.direction = "EAST"
	
	def moveLeft(self):
		if not self.direction == "EAST":
			self.direction = "WEST"
	
	def moveUp(self):
		if not self.direction == "SOUTH":
			self.direction = "NORTH"
	
	def moveDown(self):
		if not self.direction == "NORTH":
			self.direction = "SOUTH"

	def draw(self, surface):
		for index in range(len(self.positions)):
			if index == 0:
				pygame.draw.rect(surface, (0, 200, 200), pygame.Rect(self.positions[index][0] + 1, self.positions[index][1] + 1, 39, 39))
			else:
				x = 200 - (10 * index)
				if x < 0:
					x = 0
				pygame.draw.rect(surface, (0, x, 200), pygame.Rect(self.positions[index][0] + 1, self.positions[index][1] + 1, 39, 39))

class Food:
	def __init__(self, snek, rows, cols):
		init = appleInit(snek, rows, cols)
		self.xPos = init[0]
		self.x = self.xPos * 40
		self.yPos = init[1]
		self.y = self.yPos * 40

	def draw(self, surface):
		pygame.draw.rect(surface, (200, 0, 0), pygame.Rect(self.x + 1, self.y + 1, 39, 39))

class Game:
	def __init__(self):
		self.running = True
		self.width = 600
		self.height = 600
		self._display_surf = None
		self.rows = (self.height / 40)
		self.cols = (self.width / 40)
		self.snake = Snake(3, "SOUTH", (0, 0))
		self.apple = Food(self.snake, self.rows, self.cols)
		self.score = 0

	def initialize(self):
		pygame.init()
		self._display_surf = pygame.display.set_mode((self.width + 40,self.height + 40))
		pygame.display.set_caption("Snake!")
		self.running = True
		self.execute()

	def checkLegality(self, x, y):
		if outOfBounds(x, y, self.width, self.height) or hitSelf(x, y, self.snake.positions):
				self.running = False

	def finishMove(self, x, y):
		if isCollision(x, y, self.apple.x, self.apple.y):
			self.score += 1
			self.snake.length += 1

			while hitSelf(self.apple.x, self.apple.y, self.snake.positions):
				init = appleInit(self.snake, self.rows, self.cols)
				self.apple.xPos = init[0]
				self.apple.x = self.apple.xPos * 40
				self.apple.yPos = init[1]
				self.apple.y = self.apple.yPos * 40
		else:
			self.snake.positions.pop()

	def afterLoop(self):
		if self.snake.direction == "NORTH":
			newX = self.snake.curPos[0]
			newY = self.snake.curPos[1] - 40
			self.checkLegality(newX, newY)
			self.snake.positions.insert(0, (newX, newY))
			self.snake.curPos = (newX, newY)
			self.finishMove(newX, newY)
		
		elif self.snake.direction == "WEST":
			newX = self.snake.curPos[0] - 40
			newY = self.snake.curPos[1]
			self.checkLegality(newX, newY)
			self.snake.positions.insert(0, (newX, newY))
			self.snake.curPos = (newX, newY)
			self.finishMove(newX, newY)
		
		elif self.snake.direction == "EAST":
			newX = self.snake.curPos[0] + 40
			newY = self.snake.curPos[1] 
			self.checkLegality(newX, newY)
			self.snake.positions.insert(0, (newX, newY))
			self.snake.curPos = (newX, newY)
			self.finishMove(newX, newY)
		
		elif self.snake.direction == "SOUTH":
			newX = self.snake.curPos[0]
			newY = self.snake.curPos[1] + 40
			self.checkLegality(newX, newY)
			self.snake.positions.insert(0, (newX, newY))
			self.snake.curPos = (newX, newY)
			self.finishMove(newX, newY)

	def drawAll(self):
		self._display_surf.fill((0, 0, 0))
		self.snake.draw(self._display_surf)
		self.apple.draw(self._display_surf)
		pygame.display.flip()

	def execute(self):
		while self.running:
			pygame.event.pump()

			keys = pygame.key.get_pressed() 
			if (keys[K_RIGHT]):
				self.snake.moveRight()

			if (keys[K_LEFT]):
				self.snake.moveLeft()

			if (keys[K_UP]):
				self.snake.moveUp()

			if (keys[K_DOWN]):
				self.snake.moveDown()

			if (keys[K_ESCAPE]):
				self.running = False

			self.afterLoop()
			self.drawAll()
			time.sleep (100.0 / 1000.0);
		print("You lost! Score:", self.score)
		pygame.quit()

game = Game()
game.initialize()
