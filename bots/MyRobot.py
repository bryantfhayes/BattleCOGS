from bots.Bot import Bot
from util.Direction import Direction

class MyRobot(Bot):
	def __init__(self):
		Bot.__init__(self)
		self.turn = False
		self.dir_index = 0
		self.dirs = [Direction.North, Direction.East, Direction.South, Direction.West]

	def run(self):
		self.shoot()
		return
		if self.turn == False:
			self.moveForward()
		else:
			self.faceDirection(self.dirs[self.dir_index])
			self.dir_index += 1
			if self.dir_index == 4:
				self.dir_index = 0
				self.shoot()

		self.turn = not self.turn

		

