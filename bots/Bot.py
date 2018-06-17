from components.Robot import Robot
from core.EventManager import EventManager
from util.Vector2D import Vector2D
from util.Direction import Direction

class Bot(object):
	def __init__(self):
		# Default Public variables
		self.symbol = "R"
		self.direction = Direction.North
		self.action = None

		# Private variables
		self._mass = 100.0
		self._hp = 1000.0
		self._scan_range = 3

	#
	# Abstract - Configure robot once at creation. This dictates load out params
	#
	def configure(self):
		pass

	#
	# Abstract - Runs everytime robot has an action to use
	#
	def run(self, state):
		pass