from components.Component import Component

from core.EventManager import EventManager

class Health(Component):
	def __init__(self, initialHealth=100):
		Component.__init__(self)
		self.maxHealth = initialHealth
		self.health = initialHealth
		
