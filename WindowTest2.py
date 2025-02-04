import RaphaelScriptHelper as gamer
import multiprocessing
import testDict as rd
import settings
import pyautogui
import time
import GhHelper as ghh
import pygetwindow as gw
import schedule
from datetime import datetime
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
windowID3 = "BlueStacks Multi"
# 首个按钮 150%中 (900, 225), (900, 330), 确认键为 (900, 600)
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

def verify_empty():
    time.sleep(1)
    if len(gamer.find_all_empty(ghh.get_all_center())) > 0:
        return True
    else:
        return False


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
    count = 0
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
        count += 1
        if count%4 == 0:
            clean_up(1)
    process_existed_orange()

def filter_beike(count = 7):
    for i in range(1, count):
        gamer.touch(ghh.get_center((1,5)))
    process_existed(targetListBeike)

# def clean_up():
#     process_existed(targetListCoin)
#     gamer.delay(1)
#     gamer.find_pic_double_touch(rd.icon_5)
#     process_existed(targetListFloat)
#     gamer.delay(1)
#     gamer.find_pic_double_touch(rd.float_4)

def clean_up(type):
    if type == 1:
        process_existed(targetListCoin)
        gamer.delay(1)
        gamer.find_pic_double_touch(rd.icon_5)
    elif type == 2: 
        clean_up(1)
        process_existed(targetListFloat)
        gamer.delay(1)
        gamer.find_pic_double_touch(rd.float_4)
    else:
        clean_up(2)
        gamer.find_pic_double_touch(rd.icon_4)
        gamer.find_pic_double_touch(rd.icon_3)
        gamer.find_pic_double_touch(rd.float_3)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

# 简单功能测试
# temp = gamer.find_pic_all_list([rd.bubble_beike_4])
# logging.info(temp[0])
# logging.info(ghh.find_item_counts(rd.bubble_beike_4))
# logging.info(ghh.find_item_counts(rd.beike_4))
# logging.info(ghh.find_item_counts(gamer.find_pic_all_list([rd.beike_4])[0]))

# button_location = pyautogui.locateCenterOnScreen('./img/manager_start.png', confidence=0.8)
# window = gw.getWindowsWithTitle("BlueStacks Multi")[0]
# if window:
#     # 激活窗口
#     window.activate()
#     # 首个按钮 150%中 (900, 225), (900, 330), 确认键为 (900, 600)
#     button_x = window.left + 900
#     button_y = window.top + 600
#     # 移动鼠标并点击按钮
#     pyautogui.click(button_x, button_y)
#     print("按钮点击成功！")
# else:
#     print("未找到窗口，请检查窗口标题。")


def round_all():
    clean_up(2)
    filter_orange()
    for i in range(1,20):
        filter_beike()
        if(gamer.verify_pic(rd.out_of_power_1)):
            gamer.touch(rd.close_button)
            if(gamer.verify_pic(rd.out_of_power_1)):
                logging.error("未能正确离开无体力状态")
                msh.send_simple_push("1","错误：未能离开无体力状态")
                continue
            logging.info("正确离开无体力状态")
            # msh.send_simple_push("1","提示：正确离开无体力状态")
            process_existed(targetListBeike)
            clean_up(2)
            break
        if verify_empty():
            clean_up(2)
        else:
            clean_up(3)
    gamer.home()
    gamer.delay(5)  # 等待窗口激活
    gamer.find_pic_touch(rd.start_game)
    logging.info(msh.send_simple_push("1","提示：完成一轮执行"))
    logging.info("完成执行")

# 设置定时任务
schedule.every().hour.at(":00").do(round_all)  # 每小时 0 分钟
schedule.every().hour.at(":20").do(round_all)  # 每小时 20 分钟
schedule.every().hour.at(":40").do(round_all)  # 每小时 40 分钟

print("定时任务已启动，等待运行...")

# 保持程序运行
while True:
    schedule.run_pending()  # 运行待执行的任务
    time.sleep(5)  # 每5秒检查一次