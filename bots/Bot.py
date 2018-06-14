from components.Robot import Robot
from core.EventManager import EventManager
from util.Vector2D import Vector2D
from util.Direction import Direction

class Bot(object):
	def __init__(self):
		# Public variables
		self.entity = None
		self.symbol = "R"
		self.direction = Direction.North

		# Private variables
		self._emit_event = ""
		self._emit_data = {}
		self._mass = 100.0
		self._hp = 1000.0
		self._cost = 0
		self._ttr = 0

	def run(self):
		pass

	def _emit(self):
		# Add cost to TTR
		self._ttr += self._cost

		if self._emit_event != "":
			EventManager.Instance().fireEvent(self._emit_event, self._emit_data)

	##################
	# BATTLECOGS API #
	##################

	#
	# Cancel all queued commands and just sit idle until the next tick
	#
	def doNothing(self):
		self._emit_event = ""
		self._emit_data = {}
		self.cost = 0

	#
	# Shoot the currently loaded projectile in the forward facing direction
	#
	def shoot(self):
		self._emit_event = "EVENT_ShootProjectile"
		self._emit_data = {"origin" : self.entity.components["Transform2D"].position, "direction" : self.direction, "damage" : 20}
		self._cost = 30

	#
	# Turn your robot to face a specified direction
	#
	def faceDirection(self, direction):
		print("Facing direction: {}".format(direction))
		self.direction = direction
		self._cost = int((self._hp / self._mass) / 4)

	#
	# Move your robot forward by one step (in the direction you are facing)
	#
	def moveForward(self):
		print("Moving robot forward!")
		self._emit_event = "EVENT_MoveEntity"
		self._emit_data = {"entity" : self.entity, "vector2D" : Direction.getVector(self.direction)}
		self._cost = self._hp / self._mass