from bots.Bot import Bot
from util.Direction import Direction

class Human(Bot):
	def __init__(self):
		Bot.__init__(self)
		self.symbol = "H"

	def run(self, state):
		pass
		

