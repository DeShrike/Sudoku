# http://programarcadegames.com/index.php?lang=nl&chapter=introduction_to_animation
# http://programarcadegames.com/index.php?lang=nl&chapter=controllers_and_graphics
import Config
from Graphics import Graphics
from Solver import Solver

class Doku():

	def __init__(self):
		self.solver = Solver(Config.SIZE, self.callback)
		self.done = False
		self.graphics = Graphics()
		self.graphics.init("Doku Solver", Config.WINDOWSIZE)

		if Config.SIZE == 4:
			self.solver.setGrid([
				"3002",
				"0410",
				"0320",
				"4001",
			]);

		if Config.SIZE == 9:
			self.solver.setGrid([
				"000000000",
				"000000000",
				"000000000",
				"384000000",
				"000000000",
				"000000000",
				"000000000",
				"000000000",
				"000000002",
			]);

			#self.solver.setGrid([
			#	"100904082",
			#	"052680300",
			#	"864200910",
			#	"010049806",
			#	"498300701",
			#	"607010093",
			#	"086035209",
			#	"509002130",
			#	"030497008"
			#]);

		if Config.SIZE == 16:

			self.solver.setGrid([
				" D0F  63C 7 1E  ",
				"  74    B 3 D   ",
				"E 4  97 0    3AF",
				" 2     E  516B9 ",
				"B A   E  8   F  ",
				"  F CA 6        ",
				"      4     5 E ",
				" 6C7  8  5B   2 ",
				" F B9   4 C  D 2",
				" 41D 6  5     C9",
				"2   7 1 D   B  8",
				"      A83   E   ",
				"C    B9 6  20   ",
				"  2  E30   C 546",
				" A 8 C   4     1",
				" 7   5       8D "
			]);

		if Config.SIZE == 25:
			for i in range(Config.SIZE):
				self.solver.setNumber(i, i, i + 1, True)
				self.solver.setNumber(0, i, Config.SIZE - (i + 1) + 1, True)

	def callback(self):
		# self.done = True
		pass

	def run(self):
		# Loop until the user clicks the close button.
		while not self.done:

			self.done = self.graphics.queryQuit()

			# Set the screen background
			self.graphics.fill(Config.WHITE)
			# self.graphics.print("Clock: {}".format(self.graphics.fps()))

			if Config.SPEED == Config.FAST:
				# Draw everything 
				self.solver.draw(self.graphics)
				# Update screen
				self.graphics.flip()
	
			# Do physics
			self.solver.tick()

			# Draw everything 
			self.solver.draw(self.graphics)

			# Update screen
			self.graphics.flip()

		# Exit
		self.graphics.quit()

if __name__ == "__main__":
	app = Doku()
	app.run()
