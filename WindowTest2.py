import RaphaelScriptHelper as gamer
import multiprocessing
import testDict as rd
import settings
import pyautogui
import time
import GhHelper as ghh
import ImageProc
import logging
import messageHelper as msh
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
targetListBeike = [
    rd.beike_2,
    rd.beike_3,
    rd.beike_4,
    rd.beike_5,
    rd.beike_6,
    rd.beike_7,
    rd.beike_8,
    rd.beike_9,
    rd.beike_10
]

targetListFloat = [
    rd.float_2,
    rd.float_3
]
targetListCoin = [
    rd.icon_1,
    rd.icon_2,
    rd.icon_3,
    rd.icon_4
]
# gamer.home()
# powerList = gamer.find_pic_all(rd.orange_4_a)
# countNow = len(powerList)


# 基础处理单元
# while True:
#     gamer.delay(1)
#     powerCol = gamer.find_pic_all_list([
#         rd.orange_1_n,
#         rd.orange_2_n,
#         rd.orange_3_n,
#         rd.orange_4_n,
#         rd.orange_5_n,
#         rd.orange_6_n
#     ])
#     powerCol = ghh.get_collection_unique_grid_positions(powerCol)
#     print("在设备{0}中，获取目标个数: {1}".format(gamer.deviceID, powerCol))
#     slideCount = ghh.process_collection(powerCol, gamer.slide)
#     print("在设备{0}中，获取滑动次数: {1}".format(gamer.deviceID, slideCount))

# powerCol = gamer.find_pic_all_list([
#         rd.orange_tree_basic,
#         rd.orange_tree_finish,
#         rd.orange_tree_loading
#     ])

def process_existed_orange():
    slideCount = 1
    while slideCount > 0:
        gamer.delay(1)
        powerCol = gamer.find_pic_all_list([
            rd.orange_1_n,
            rd.orange_2_n,
            rd.orange_3_n,
            rd.orange_4_n,
            rd.orange_5_n,
            rd.orange_6_n
        ])
        powerCol = ghh.get_collection_unique_grid_positions(powerCol)
        print("在设备{0}中，获取目标个数: {1}".format(gamer.deviceID, powerCol))
        slideCount = ghh.process_collection(powerCol, gamer.slide)
        print("在设备{0}中，获取滑动次数: {1}".format(gamer.deviceID, slideCount))

def process_existed(targetList):
    gamer.delay(1)
    powerCol = gamer.find_pic_all_list(targetList)
    powerCol = ghh.get_collection_unique_grid_positions(powerCol)
    print("在设备{0}中，获取目标个数: {1}".format(gamer.deviceID, powerCol))
    slideCount = ghh.process_collection(powerCol, gamer.slide)
    print("在设备{0}中，获取滑动次数: {1}".format(gamer.deviceID, slideCount))


# temp = ImageProc.get_color(rd.empty_blue_2,(64,64))
# print("在设备{0}中，获取目标个数: {1}".format(gamer.deviceID, powerCol[0]))
# temp = gamer.find_all_empty(ghh.get_all_center())
# print("temp:{0}".format(temp))

# 点击贝壳发射器
# gamer.touch(ghh.get_center((1,5)))


# 此处为收橘子完整逻辑
def filter_orange():
    treeCol = gamer.find_pic_all_list([
            rd.orange_tree_todo
        ])
    treeCol = ghh.get_collection_unique_grid_positions(treeCol)
    print("在设备{0}中，获取橘子树总数: {1}".format(gamer.deviceID, len(treeCol[0])))
    for tree in treeCol[0]:
        while True:
            gamer.touch(tree)
            if(gamer.verify_pic(rd.general_current_loading)):
                break
            gamer.touch(tree)
            gamer.touch(tree)
            gamer.touch(tree)
            gamer.touch(tree)
            gamer.touch(tree)
            gamer.touch(tree)
            # if(len(gamer.find_all_empty(ghh.get_all_center())) > 0):
            #     print("点击后依旧有空间，继续新一轮点击")
            #     break
            process_existed_orange()   
    process_existed_orange()

def filter_beike(count = 7):
    for i in range(1, count):
        gamer.touch(ghh.get_center((1,5)))
    process_existed(targetListBeike)

def clean_up():
    process_existed(targetListCoin)
    gamer.find_pic_double_touch(rd.icon_5)
    process_existed(targetListFloat)
    gamer.find_pic_double_touch(rd.float_4)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

temp = gamer.find_pic_all_list([rd.bubble_beike_4])
logging.info(temp[0])
logging.info(ghh.find_item_counts(rd.bubble_beike_4))
logging.info(ghh.find_item_counts(rd.beike_4))
# logging.info(ghh.find_item_counts(gamer.find_pic_all_list([rd.beike_4])[0]))

# filter_orange()
# for i in range(1,20):
#     filter_beike()
#     if(gamer.verify_pic(rd.out_of_power_1)):
#         gamer.touch(rd.close_button)
#         if(gamer.verify_pic(rd.out_of_power_1)):
#             logging.error("未能正确离开无体力状态")
#             msh.send_simple_push("未能正确离开无体力状态","错误")
#             continue
#         logging.info("正确离开无体力状态")
#         msh.send_simple_push("正确离开无体力状态","提示")
#         process_existed(targetListBeike)
#         clean_up()
#         break
#     clean_up()

