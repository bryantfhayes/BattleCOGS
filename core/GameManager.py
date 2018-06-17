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

healthLookupTable = {
    "X" : 9999999,
    "#" : 200
}

@Singleton
class GameManager(object):
    def __init__(self):
        self.updateBuffer = 0
        self.entitymap = {}
        self.map_size_x = 0
        self.map_size_y = 0

    def Init(self, tps=100):
        # Setup links between the various managers
        SystemManager.Instance().Init()
        EntityManager.Instance().Init()
        EventManager.Instance().Init()

        self.tps = tps
        self.lastUpdated = time.time()
        self.running = True
        self.message_log = []
        self.cached_map = []

    def refreshCachedMap(self):
        self.cached_map = []
        for col in xrange(self.map_size_x):
            row_arr = []
            for row in xrange(self.map_size_y):
                row_arr.append([])
            self.cached_map.append(row_arr)

        for e, component in EntityManager.Instance().pairs_for_type(Transform2D):
            self.cached_map[component.position.x][component.position.y].append(e)

    #
    # @brief Load map as individual entities
    # 
    def loadMap(self, mapArr):
        self.map_size_x = len(mapArr[0])
        self.map_size_y = len(mapArr)
        print("Map Size: ({0}, {1})".format(self.map_size_x, self.map_size_y))
        for row in range(0, len(mapArr)):
            for col in range(0, len(mapArr[0])):
                if mapArr[row][col] in list(healthLookupTable.keys()):
                    entity = EntityManager.Instance().create_entity(mapArr[row][col])
                    EntityManager.Instance().add_component(entity, Transform2D(Vector2D(col, row)))
                    EntityManager.Instance().add_component(entity, Health(healthLookupTable[mapArr[row][col]]))
                
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


