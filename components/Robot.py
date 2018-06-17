from components.Component import Component

from core.EventManager import EventManager
from core.GameManager import GameManager
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

	#
	# Return a scan of the surrounding area, range depends on the range of the robot scanning
	#
	def _scan(self):
		scan_results = []
		GameManager.Instance().refreshCachedMap()
		cached_map = list(GameManager.Instance().cached_map)
		rng = self.bot._scan_range
		posX = self.entity.components["Transform2D"].position.x
		posY = self.entity.components["Transform2D"].position.y
		lowerX = max(posX - rng, 0)
		lowerY = max(posY - rng, 0)
		print(GameManager.Instance().map_size_x, GameManager.Instance().map_size_y, self.entity.components["Transform2D"].position.y)
		upperX = min(posX + rng, GameManager.Instance().map_size_x-1)
		upperY = min(posY + rng, GameManager.Instance().map_size_y-1)
		for col in xrange(lowerX, upperX + 1):
			for row in xrange(lowerY, upperY + 1):
				# TODO: COuld be a bug because this assumes no entity can be found on the same tile as your robot.
				if len(cached_map[col][row]) > 0:
					if self.entity in cached_map[col][row]:
						cached_map[col][row].remove(self.entity)
						continue
					scan_results.append((Vector2D(row, col), cached_map[col][row]))

		return scan_results

	def _apiCallBegin(self):
		pass

	def _apiCallEnd(self):
		self._emit_event = ""
		self._emit_data = {}

	##################
	# BATTLECOGS API #
	##################

	#
	# Cancel all queued commands and just sit idle until the next tick
	#
	def doNothing(self):
		self._apiCallBegin()
		self._emit_event = ""
		self._emit_data = {}
		self._cost = 0
		self._apiCallEnd()

	#
	# Shoot the currently loaded projectile in the forward facing direction
	#
	def shoot(self):
		self._apiCallBegin()
		self._emit_event = "EVENT_ShootProjectile"
		self._emit_data = {"origin" : self.entity.components["Transform2D"].position, "direction" : self.bot.direction, "damage" : 20}
		self._cost = 30
		self._apiCallEnd()

	#
	# Turn your robot to face a specified direction
	#
	def faceDirection(self, direction):
		self._apiCallBegin()
		self.direction = direction
		self._cost = int((self.bot._hp / self.bot._mass) / 4)
		self._apiCallEnd()

	#
	# Move your robot forward by one step (in the direction you are facing)
	#
	def moveForward(self):
		self._apiCallBegin()
		self._emit_event = "EVENT_MoveEntity"
		self._emit_data = {"entity" : self.entity, "vector2D" : Direction.getVector(self.bot.direction)}
		self._cost = self.bot._hp / self.bot._mass
		self._apiCallEnd()
