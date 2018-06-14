from core.GameManager import GameManager
from core.EventManager import EventManager
from core.SystemManager import SystemManager
from core.EntityManager import EntityManager

from systems.Input import Input
from systems.Renderer import Renderer, Panel
from systems.Physics import Physics
from systems.RobotControl import RobotControl
from systems.Combat import Combat

from components.Transform2D import Transform2D
from components.Health import Health
from components.Robot import Robot
from components.Collider import *

from bots.MyRobot import MyRobot

from util.Vector2D import Vector2D
import util.Colors as Colors

import random

class BattleCOGS():
    def __init__(self):
        pass

    def init(self):
        self.robots = []

        GameManager.Instance().Init()

        # Apply all sub-systems to system manager
        SystemManager.Instance().add_system(Input(), priority=1)
        SystemManager.Instance().add_system(Renderer(110, 50), priority=0)
        SystemManager.Instance().add_system(Physics(), priority=5)
        SystemManager.Instance().add_system(RobotControl(), priority=4)
        SystemManager.Instance().add_system(Combat(), priority=3)

        # Setup GUI
        renderer = SystemManager.Instance().get_system_of_type(Renderer)

        # Add panels
        renderer.addPanel(Panel(renderer.window, renderer.screen_width - 20, 0, 20, renderer.screen_height - 7, Panel.Right, "EVENT_StatsUpdated", renderer))
        EventManager.Instance().fireEvent("EVENT_StatsUpdated", [{"HP: 10/10" : {"color" : Colors.gold}},
                                                                 {"MP:  5/20" : {"color" : Colors.gold}}])
        renderer.addPanel(Panel(renderer.window, 0, renderer.screen_height - 7, renderer.screen_width, 7, Panel.Bottom, "EVENT_ConsoleMessageAdded", renderer))
        GameManager.Instance().message("Hello, this is my first console message!")

    def add_robot(self, type, x, y):
        # Create a bot and link back the entity so that user can reference other components
        bot = type()
        robot = EntityManager.Instance().create_entity(bot.symbol, z=10)
        bot.entity = robot

        EntityManager.Instance().add_component(robot, Transform2D(Vector2D(x, y)))
        EntityManager.Instance().add_component(robot, Health())
        EntityManager.Instance().add_component(robot, Collider(COLLIDER_PLAYER, COLLIDER_PLAYER | COLLIDER_WALL))
        EntityManager.Instance().add_component(robot, Robot(bot))
        GameManager.Instance().message("Bryant entered the strange room hesitantly.", Colors.red)
        self.robots.append(robot)

        EventManager.Instance().fireEvent("EVENT_StatsUpdated", [{"HP: {0}/{1}".format(robot.components["Health"].health, robot.components["Health"].maxHealth) : {"color" : Colors.gold}},
                                                                 {"MP:  5/20" : {"color" : Colors.gold}}])

    def load_map(self, filename):
        mapArr = []
        count = 0
        with open(filename, 'r') as fp:
            lines = fp.readlines()
            for line in lines:
                mapArr.append([])
                for char in line.strip('\n'):
                    mapArr[count].append(char)
                count += 1
        GameManager.Instance().loadMap(mapArr)

    def onKeyPressed(self, args):
        char = args["char"]
        v = None

        GameManager.Instance().message("Bryant pressed a button: {}".format(char), Colors.green)

        if char == "UP":
            v = Vector2D(0, -1)
        elif char == "LEFT":
            v = Vector2D(-1, 0)
        elif char == "RIGHT":
            v = Vector2D(1, 0)
        elif char == "DOWN":
            v = Vector2D(0, 1)
        elif char == "S":
            for bot in self.robots:
                EventManager.Instance().fireEvent("EVENT_ShootProjectile", {"origin" : bot.components["Transform2D"].position, "direction" : bot.components["Robot"].bot.direction, "damage" : 20})
                return
        elif char == "F":
            for bot in self.robots:
                EventManager.Instance().fireEvent("EVENT_FocusCameraOnEntity", bot)
            return
        elif char == "G":
            EventManager.Instance().fireEvent("EVENT_FocusCameraOnEntity", None)
            return
        else:
            return

        for bot in self.robots:
            EventManager.Instance().fireEvent("EVENT_MoveEntity", {"entity" : bot, "vector2D" : v})

    #
    # @brief Quit the game
    # 
    def quitCallback(self, args):
        GameManager.Instance().running = False

    def run(self):
        pass

#
# @brief Entry Point
# 
def main():
    battlecogs = BattleCOGS()

    # Setup game systems
    battlecogs.init()

    # DO GAME LOGIC STUFF #

    # Create a player
    battlecogs.add_robot(MyRobot, random.randint(5, 10), random.randint(5, 10))
    battlecogs.add_robot(MyRobot, random.randint(5, 10), random.randint(5, 10))

    # Load map
    battlecogs.load_map("assets/level_1.txt")

    # Get key presses
    EventManager.Instance().subscribe("EVENT_KeyPressed", battlecogs.onKeyPressed)

    # END GAME LOGIC STUFF #

    # Register game over callback on "Q" being pressed
    EventManager.Instance().subscribe("EVENT_QuitGame", battlecogs.quitCallback)

    # Run game
    GameManager.Instance().run()

if __name__ == "__main__":
    main()