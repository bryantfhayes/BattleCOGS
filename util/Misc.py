# Determine if a number is within a specified range
def numInRange(x, a, b, exclusive=False):
	if exclusive:
		if x > a and x < b:
			return True
		else:
			return False
	else:
		if x >= a and x <= b:
			return True
		else:
			return False

# Determine if a vector is within a specified range
def vectorInRange(vect, x0, x1, y0, y1, exclusive=False):
	if exclusive:
		if vect.x > x0 and vect.y > y0 and vect.x < x1 and vect.y < y1:
			return True
		else:
			return False
	else:
		if vect.x >= x0 and vect.y >= y0 and vect.x <= x1 and vect.y <= y1:
			return True
		else:
			return False