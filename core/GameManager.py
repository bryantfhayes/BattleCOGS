from core.EntityManager import EntityManager
from core.SystemManager import SystemManager
from core.EventManager import EventManager
from core.Singleton import Singleton

from components.Transform2D import Transform2D
from components.Health import Health
from components.Collider import *
from components.Collider import Collider

import util.Colors as Colors
from util.Vector2D import Vector2D

import time

@Singleton
class GameManager(object):
    def __init__(self):
        self.updateBuffer = 0
        self.arr = []

    def Init(self, tps=10):
        # Setup links between the various managers
        SystemManager.Instance().Init()
        EntityManager.Instance().Init()
        EventManager.Instance().Init()

        self.tps = tps
        self.lastUpdated = time.time()
        self.running = True
        self.message_log = []

    #
    # @brief Load map as individual entities
    # 
    def loadMap(self, mapArr):
        for row in range(0, len(mapArr)):
            for col in range(0, len(mapArr[0])):
                entity = EntityManager.Instance().create_entity(mapArr[row][col])
                EntityManager.Instance().add_component(entity, Transform2D(Vector2D(col, row)))
                EntityManager.Instance().add_component(entity, Health())
                if entity.symbol == "#":
                    EntityManager.Instance().add_component(entity, Collider(COLLIDER_WALL, COLLIDER_PLAYER | COLLIDER_WALL | COLLIDER_PROJECTILE))

    #
    # @brief Send notification containing the latest message log
    # 
    def message(self, msg, color=Colors.white):
        self.message_log.append({msg : {"color" : color}})
        EventManager.Instance().fireEvent("EVENT_ConsoleMessageAdded", self.message_log)

    #
    # @brief Run the game!
    # 
    def run(self):
        while (self.running):
            currentTime = time.time()
            delta = currentTime - self.lastUpdated
            self.updateBuffer += delta
            self.lastUpdated = currentTime

            # Update at designated interval
            if self.updateBuffer >= (1.0 / self.tps):
                SystemManager.Instance().update(self.updateBuffer)
                self.updateBuffer = 0


