import RaphaelScriptHelper as gamer
import multiprocessing
import testDict as rd
import settings
import pyautogui
import time
import ADBHelper
from enum import Enum

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

windowID = "BlueStacks App Main"
windowID2 = "BlueStacks App Player 2"
windowID3 = "BlueStacks Multi"
deviceID = "emulator-5554"
deviceID2 = "emulator-5574"
deviceID2 = "127.0.0.1:5595"
manager_pos_1 = (900, 225)
manager_pos_2 = (900, 330)
manager_pos_submit = (900, 600)

gamer.deviceID = deviceID
# gamer.home()
# powerList = gamer.debug_find_pic_all(rd.power_4)
# countNow = len(powerList)
# print("在设备{0}中，获取目标个数: {1}".format(gamer.deviceID, countNow))

def restart_all():
    gamer.bs_manager_click(windowID3, manager_pos_1)
    gamer.delay(1)
    gamer.bs_manager_click(windowID3, manager_pos_submit)
    gamer.delay(1)
    gamer.bs_manager_click(windowID3, manager_pos_2)
    gamer.delay(1)
    gamer.bs_manager_click(windowID3, manager_pos_submit)
    gamer.delay(10)
    gamer.bs_manager_click(windowID3, manager_pos_1)
    gamer.delay(5)
    gamer.bs_manager_click(windowID3, manager_pos_2)
    gamer.delay(40)

ADBHelper.connent(deviceID2)

