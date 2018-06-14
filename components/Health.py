from components.Component import Component

from core.EventManager import EventManager

class Health(Component):
	def __init__(self):
		Component.__init__(self)
		self.maxHealth = 100
		self.health = 100

	def changeMaxHealth(self, newMax):
		self.maxHealth = newMax

	def takeDamage(self, dmg):
		self.health -= dmg
		if self.health <= 0:
			EventManager.Instance().fireEvent("EVENT_PlayerDied")
