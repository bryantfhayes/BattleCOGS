from components.Component import Component

from core.EventManager import EventManager

class Health(Component):
	def __init__(self):
		Component.__init__(self)
		self.maxHealth = 100
		self.health = 100
		
