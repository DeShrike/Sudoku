import Config
import math
from Graphics import Graphics

class Item():

	def __init__(self, x, y, number, fixed = False):
		self.x = x
		self.y = y
		self.number = number
		self.fixed = fixed

	def __repr__(self):
		return f"Item({self.x}, {self.y}, {self.number}, {self.fixed})"

class Solver():

	def __init__(self, size, callback):
		self.size = size  	# 4 of 9 of 16
		self.callback = callback
		self.done = False
		self.grid = [[ None for _ in range(self.size) ] for _ in range(self.size)]
		self.stack = []
		self.popped = False
		self.steps = 0

	def callback(self):
		# self.done = True
		pass

	def setGrid(self, grid):
		for y in range(self.size):
			line = grid[y]
			for x in range(self.size):
				num = int(line[x])
				if num != 0:
					self.setNumber(x, y, num, True)

	def setNumber(self, x, y, number, fixed = False):
		self.grid[y][x] = Item(x, y, number, fixed)

	def toDisplay(self, number):
		if self.size == 25:
			return chr(ord("A") + number - 1)
		if number == 0 or number == None:
			return " "
		if number < 10:
			return str(number)
		return chr(ord("A") + number - 10)

	def draw(self, graphics):

		for y in range(self.size):
			for x in range(self.size):
				if self.grid[y][x] != None and self.grid[y][x].number != 0:
					xx = (x * Config.GRIDSIZE) + (Config.GRIDSIZE // 2)
					yy = (y * Config.GRIDSIZE) + (Config.GRIDSIZE // 2)
					if self.grid[y][x].fixed:
						graphics.rectangle((x * Config.GRIDSIZE), (y * Config.GRIDSIZE), Config.GRIDSIZE, Config.GRIDSIZE, Config.GRAY)
					graphics.printCentered(xx, yy, self.toDisplay(self.grid[y][x].number))

		for i in range(self.size + 1):
			x = Config.GRIDSIZE * i
			lw = 3 if i % int(math.sqrt(Config.SIZE)) == 0 else 1
			graphics.line(x, 0, x, Config.HEIGHT, lw, (0, 0, 0))
			graphics.line(0, x, Config.WIDTH, x, lw, (0, 0, 0))

	def push(self, item):
		self.stack.append(item)
		self.grid[item.y][item.x] = item

	def pop(self):
		item = self.stack.pop()
		self.grid[item.y][item.x] = None
		return item

	def doStep(self):

		print(self.steps, end = "\r")
		self.steps += 1
		
		if self.popped:
			self.popped = False
			if len(self.stack) == 0:
				self.done = True

				if self.isAllDone():
					print("Found a solution !")
					return

				print("No solution")
				return
			item = self.stack[-1]
			item = self.advanceSpot(item)
			if item == None:
				self.pop()
				self.popped = True
		else:
			item = self.findSpot()
			if item == None:
				self.pop()
				self.popped = True
			else:
				self.push(item)
		# a = input()

	def tick(self):
		if self.done:
			return

		if self.isAllDone():
			self.done = True
			print("Found a solution !")
			return

		if Config.SPEED == Config.SLOW:
			self.doStep()
		elif Config.SPEED == Config.MEDIUM:
			for _ in range(1000):
				self.doStep()
		elif Config.SPEED == Config.FAST:
			while not self.done:
				self.doStep()

	def advanceSpot(self, item):
		if item.number == self.size:
			return None
		for i in range(item.number + 1, self.size + 1):
			item.number = i
			if self.isValid(item):
				return item
		return None

	def findSpot(self):
		for y in range(self.size):
			for x in range(self.size):
				if self.grid[y][x] == None:
					for i in range(1, self.size + 1):
						item = Item(x, y, i)
						if self.isValid(item):
							return item
					return None
		return None

	def isValid(self, item):
		return self.isValidVertical(item) and self.isValidHorizontal(item) and self.isValidBox(item)

	def isValidVertical(self, item):
		for y in range(self.size):
			i = self.grid[y][item.x]
			if y == item.y:
				continue;
			if i == None:
				continue
			if item.number == i.number:
				return False

		return True

	def isValidHorizontal(self, item):
		for x in range(self.size):
			i = self.grid[item.y][x]
			if x == item.x:
				continue
			if i == None:
				continue
			if item.number == i.number:
				return False
		
		return True

	def isValidBox(self, item):
		# print(item)
		q = int(math.sqrt(self.size))
		sx = (item.x // q) * q
		sy = (item.y // q) * q
		# print(f"{sx} {sy} {q}")
		# input()
		for y in range(sy, sy + q):
			for x in range(sx, sx + q):
				i = self.grid[y][x]
				if x == item.x and y == item.y:
					continue
				if i == None:
					continue
				if item.number == i.number:
					return False

		return True

	def isAllDone(self):
		for y in range(self.size):
			for x in range(self.size):
				if self.grid[y][x] == None:
					return False
		return True
