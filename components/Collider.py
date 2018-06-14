from components.Component import Component

# Collider masks
COLLIDER_PLAYER = 0b00000001
COLLIDER_WALL = 0b000000010

class Collider(Component):
	def __init__(self, mask, collidesWithMask):
		Component.__init__(self)
		self.mask = mask
		self.collidesWithMask = collidesWithMask
