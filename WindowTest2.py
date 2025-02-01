import RaphaelScriptHelper as gamer
import multiprocessing
import testDict as rd
import settings
import pyautogui
import time
from enum import Enum

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

windowID = "BlueStacks App Main"
windowID2 = "BlueStacks App Player 2"
deviceID = "emulator-5554"
deviceID2 = "emulator-5574"

gamer.deviceID = deviceID
powerList = gamer.find_pic_all(rd.power_4)
countNow = len(powerList)
print("在设备{0}中，获取4级体力瓶个数: {1}".format(gamer.deviceID, countNow))