import RaphaelScriptHelper as gamer
import multiprocessing
import testDict as rd
import settings
import pyautogui
from enum import Enum

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

windowID2 = "BlueStacks App Player 2"

gamer.init_window_save(windowID2)
# bs_press h-断网 1-返回主页
gamer.bs_press('h')