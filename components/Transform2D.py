from components.Component import Component

from util.Vector2D import Vector2D

class Transform2D(Component):
	def __init__(self, position=Vector2D(0, 0)):
		Component.__init__(self)
		self.position = position