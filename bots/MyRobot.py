from bots.Bot import Bot
from util.Direction import Direction

class MyRobot(Bot):
	def __init__(self):
		Bot.__init__(self)
		self.symbol = "M"

	def configure(self):
		return

	def run(self, state):
		scan = state["scan"]
		print("----------------------")
		for s in scan:
			print(s)
		#self.action.shoot()
		return

		

