from components.Component import Component

from core.EventManager import EventManager

class Robot(Component):
	def __init__(self, bot):
		Component.__init__(self)
		self.bot = bot
