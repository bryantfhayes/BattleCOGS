from systems.System import System

from components.Transform2D import Transform2D
from components.Collider import Collider
from components.Robot import Robot
from components.Projectile import Projectile
from components.Health import Health

from core.EventManager import EventManager
from core.SystemManager import SystemManager
from core.EntityManager import EntityManager
from core.GameManager import GameManager

from util.Vector2D import Vector2D
import util.Colors as Colors

from components.Collider import *

class Combat(System):
    def __init__(self):
        System.__init__(self)

    def init(self):
        EventManager.Instance().subscribe("EVENT_DealDamage", self.dealDamage)

    def dealDamage(self, args):
        attacker = args["attacker"]
        attacked = args["attacked"]
        damage = args["damage"]

        if "Health" in attacked.components:
            attacked.components["Health"].health -= damage
            if attacked.components["Health"].health <= 0:
                attacked.removable = True

            GameManager.Instance().message("{0} hit {1} for {2} damage ({3} / {4})".format(attacker, attacked, damage, attacked.components["Health"].health, attacked.components["Health"].maxHealth), Colors.red)
        
    def update(self, dt):
        pass