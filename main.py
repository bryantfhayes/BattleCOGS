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

from util.Vector2D import Vector2D
import util.Colors as Colors

import random, importlib, sys

player = None

class BattleCOGS():
    def __init__(self, bot1, bot2):
        pass

    def init(self):
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
        bot.action = Robot(robot, bot)

        EntityManager.Instance().add_component(robot, Transform2D(Vector2D(x, y)))
        EntityManager.Instance().add_component(robot, Health())
        EntityManager.Instance().add_component(robot, Collider(COLLIDER_PLAYER, COLLIDER_PLAYER | COLLIDER_WALL))
        EntityManager.Instance().add_component(robot, bot.action)
        GameManager.Instance().message("Bryant entered the strange room hesitantly.", Colors.red)

        EventManager.Instance().fireEvent("EVENT_StatsUpdated", [{"HP: {0}/{1}".format(robot.components["Health"].health, robot.components["Health"].maxHealth) : {"color" : Colors.gold}},
                                                                 {"MP:  5/20" : {"color" : Colors.gold}}])
        return robot

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

        GameManager.Instance().message("You pressed a button: {}".format(char), Colors.green)

        if char == "UP":
            v = Vector2D(0, -1)
        elif char == "LEFT":
            v = Vector2D(-1, 0)
        elif char == "RIGHT":
            v = Vector2D(1, 0)
        elif char == "DOWN":
            v = Vector2D(0, 1)
        elif char == "S":
            for e, component in EntityManager.Instance().pairs_for_type(Robot):
                EventManager.Instance().fireEvent("EVENT_ShootProjectile", {"origin" : e.components["Transform2D"].position, "direction" : e.components["Robot"].bot.direction, "damage" : 20})
                return
        elif char == "1":
            robots = []
            for e, component in EntityManager.Instance().pairs_for_type(Robot):
                robots.append(e)
            if len(robots) >= 1:
                EventManager.Instance().fireEvent("EVENT_FocusCameraOnEntity", robots[0])
            return
        elif char == "2":
            robots = []
            for e, component in EntityManager.Instance().pairs_for_type(Robot):
                robots.append(e)
            if len(robots) >= 2:
                EventManager.Instance().fireEvent("EVENT_FocusCameraOnEntity", robots[1])
            return
        elif char == "G":
            EventManager.Instance().fireEvent("EVENT_FocusCameraOnEntity", None)
            return
        else:
            return

        for e, component in EntityManager.Instance().pairs_for_type(Robot):
            EventManager.Instance().fireEvent("EVENT_MoveEntity", {"entity" : e, "vector2D" : v})

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
    global player

    # Parse command line for robots
    if len(sys.argv) != 3:
        print("USAGE: python main.py [BOT1] [BOT2]")
        exit()
    bot1 = sys.argv[1]
    bot2 = sys.argv[2]
    b1 = importlib.import_module("bots." + bot1)
    b2 = importlib.import_module("bots." + bot2)

    battlecogs = BattleCOGS(bot1, bot2)

    # Setup game systems
    battlecogs.init()

    # DO GAME LOGIC STUFF #

    # Create a player
    battlecogs.add_robot(getattr(b1, bot1), 15, 9)
    battlecogs.add_robot(getattr(b2, bot2), 30, 9)

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