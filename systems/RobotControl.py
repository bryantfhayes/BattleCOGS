from systems.System import System

from components.Transform2D import Transform2D
from components.Collider import Collider
from components.Robot import Robot
from components.Projectile import Projectile

from core.EventManager import EventManager
from core.SystemManager import SystemManager
from core.EntityManager import EntityManager
from core.GameManager import GameManager

from util.Vector2D import Vector2D
from util.Direction import Direction
import util.Colors as Colors

from components.Collider import *

class RobotControl(System):
    def __init__(self):
        System.__init__(self)

    def init(self):
        EventManager.Instance().subscribe("EVENT_ShootProjectile", self.spawnProjectile)

    def spawnProjectile(self, args):
        origin = args["origin"]
        direction = args["direction"]
        damage = args["damage"]

        p = EntityManager.Instance().create_entity("+", z=9)
        EntityManager.Instance().add_component(p, Transform2D(origin + Direction.getVector(direction)))
        EntityManager.Instance().add_component(p, Projectile(damage, direction))
        EntityManager.Instance().add_component(p, Collider(COLLIDER_PROJECTILE, COLLIDER_PLAYER | COLLIDER_WALL))
        GameManager.Instance().message("A bullet shot rings through the air!", Colors.yellow)

    def update(self, dt):
        # Iterate over every robot
        for e, robot in EntityManager.Instance().pairs_for_type(Robot):
            if robot._ttr <= 0:
                robot.bot.run()
                robot._emit()
            else:
                robot._ttr -= 1