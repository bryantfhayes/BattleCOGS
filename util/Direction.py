from enum import Enum
from util.Vector2D import Vector2D

class Direction(Enum):
    North = "North"
    West = "West"
    East = "East"
    South = "South"

    @staticmethod
    def getVector(dir):
        if dir == "North":
            return Vector2D(0, -1)
        elif dir == "West":
            return Vector2D(-1, 0)
        elif dir == "East":
            return Vector2D(1, 0)
        elif dir == "South":
            return Vector2D(0, 1)
        else:
            return Vector2D(0, 0)