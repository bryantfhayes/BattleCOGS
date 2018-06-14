from core.GameManager import GameManager
from core.EventManager import EventManager
from core.SystemManager import SystemManager
from core.EntityManager import EntityManager

from systems.Input import Input
from systems.Renderer import Renderer, Panel
from systems.Physics import Physics

from components.Transform2D import Transform2D
from components.Health import Health
from components.Collider import *

from util.Vector2D import Vector2D
import util.Colors as Colors

player = None

#
# @brief Initialize the scene
# 
def init():
    GameManager.Instance().Init()

    # Apply all sub-systems to system manager
    SystemManager.Instance().add_system(Input(), priority=0)
    SystemManager.Instance().add_system(Renderer(110, 50), priority=0)
    SystemManager.Instance().add_system(Physics(), priority=0)

    # Setup GUI
    renderer = SystemManager.Instance().get_system_of_type(Renderer)

    # Add panels
    renderer.addPanel(Panel(renderer.window, renderer.screen_width - 20, 0, 20, renderer.screen_height - 7, Panel.Right, "EVENT_StatsUpdated", renderer))
    EventManager.Instance().fireEvent("EVENT_StatsUpdated", [{"HP: 10/10" : {"color" : Colors.gold}},
                                                             {"MP:  5/20" : {"color" : Colors.gold}}])

    renderer.addPanel(Panel(renderer.window, 0, renderer.screen_height - 7, renderer.screen_width, 7, Panel.Bottom, "EVENT_ConsoleMessageAdded", renderer))
    GameManager.Instance().message("Hello, this is my first console message!")

#
# @brief Create the main player
# 
def create_player(sym, x, y):
    global player
    player = EntityManager.Instance().create_entity(sym, z=10)
    EntityManager.Instance().add_component(player, Transform2D(Vector2D(x, y)))
    EntityManager.Instance().add_component(player, Health())
    EntityManager.Instance().add_component(player, Collider(COLLIDER_PLAYER, COLLIDER_PLAYER | COLLIDER_WALL))
    GameManager.Instance().message("Bryant entered the strange room hesitantly.", Colors.red)

#
# @brief Callback called when the user pressed a key
# 
def onKeyPressed(args):
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
    elif char == "F":
        EventManager.Instance().fireEvent("EVENT_FocusCameraOnEntity", player)
        return
    elif char == "G":
        EventManager.Instance().fireEvent("EVENT_FocusCameraOnEntity", None)
        return
    else:
        return

    EventManager.Instance().fireEvent("EVENT_MoveEntity", {"entity" : player, "vector2D" : v})

def load_map(filename):
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

#
# @brief Quit the game
# 
def quitCallback(args):
    GameManager.Instance().running = False

#
# @brief Entry Point
# 
def main():
    global player

    # Setup game systems
    init()

    # DO GAME LOGIC STUFF #

    # Create a player
    create_player('@', 14, 14)
    create_player('B', 15, 15)

    # Load map
    load_map("assets/level_1.txt")

    # Get key presses
    EventManager.Instance().subscribe("EVENT_KeyPressed", onKeyPressed)

    # END GAME LOGIC STUFF #

    # Register game over callback on "Q" being pressed
    EventManager.Instance().subscribe("EVENT_QuitGame", quitCallback)

    # Run game
    GameManager.Instance().run()

if __name__ == "__main__":
    main()