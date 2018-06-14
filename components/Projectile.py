from components.Component import Component

from core.EventManager import EventManager

class Projectile(Component):
	def __init__(self, damage, direction):
		Component.__init__(self)
		self.damage = damage
		self.direction = direction