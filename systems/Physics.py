from systems.System import System

from components.Transform2D import Transform2D
from components.Collider import Collider

from core.EventManager import EventManager
from core.SystemManager import SystemManager
from core.EntityManager import EntityManager
from core.GameManager import GameManager

from util.Vector2D import Vector2D
import util.Colors as Colors

class Physics(System):
	def __init__(self):
		System.__init__(self)

	def init(self):
		EventManager.Instance().subscribe("EVENT_MoveEntity", self.attemptMove)

	def collision(self, a, b):
		msg = "{0} collided with {1}".format(a, b)
		GameManager.Instance().message(msg, color=Colors.red)

	def attemptMove(self, args):
		entity = args["entity"]
		transform = EntityManager.Instance().component_for_entity(entity, Transform2D)
		collider = EntityManager.Instance().component_for_entity(entity, Collider)
		if transform != None:
			vector2D = args["vector2D"]
			newPosition = transform.position + vector2D
			
			# Check for collisions
			for e, component in EntityManager.Instance().pairs_for_type(Collider):
				if e != entity and newPosition == e.components["Transform2D"].position and collider != None:
					if collider.mask & component.collidesWithMask:
						self.collision(entity, e)
						return

			# No collisions, so it is okay to move!
			transform.position = newPosition

	def update(self, dt):
		pass