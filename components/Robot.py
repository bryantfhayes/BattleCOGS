from components.Component import Component

from core.EventManager import EventManager
from util.Vector2D import Vector2D
from util.Direction import Direction

class Robot(Component):
	def __init__(self, entity, bot):
		Component.__init__(self)
		self.entity = entity
		self.bot = bot
		self._emit_event = ""
		self._emit_data = {}
		self._cost = 0
		self._ttr = 0

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
		self._cost = 0

	#
	# Shoot the currently loaded projectile in the forward facing direction
	#
	def shoot(self):
		self._emit_event = "EVENT_ShootProjectile"
		self._emit_data = {"origin" : self.entity.components["Transform2D"].position, "direction" : self.bot.direction, "damage" : 20}
		self._cost = 30

	#
	# Turn your robot to face a specified direction
	#
	def faceDirection(self, direction):
		self.direction = direction
		self._cost = int((self.bot._hp / self.bot._mass) / 4)

	#
	# Move your robot forward by one step (in the direction you are facing)
	#
	def moveForward(self):
		self._emit_event = "EVENT_MoveEntity"
		self._emit_data = {"entity" : self.entity, "vector2D" : Direction.getVector(self.bot.direction)}
		self._cost = self.bot._hp / self.bot._mass
