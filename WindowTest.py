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
# gamer.deviceID = "emulator-5554"

# 完整刷新流程
def reset_sub_device():
    gamer.deviceID = deviceID2
    if (not gamer.init_window_save(windowID2)): raise Exception(f'切换页面失败, 未能定位到窗口: {windowID2}')
    # bs_press h-断网 1-返回主页
    gamer.bs_press('1')
    time.sleep(0.5)
    gamer.find_pic_touch(rd.start_game)
    
    # 验证重新刷新
    # while True:
    #     time.sleep(0.5)  # 等待窗口激活
    #     if(gamer.verify_pic(rd.init_loading)):
    #         print("在设备{0}中，成功重新刷新".format(gamer.deviceID))
    #         break

    # 验证进入页面
    while True:
        time.sleep(0.5)  # 等待窗口激活
        if(gamer.verify_pic(rd.cloud_button)):
            time.sleep(3)  # 等待云端数据可选
            gamer.find_pic_touch(rd.cloud_button)
            time.sleep(5)  # 等待云端数据可选
            gamer.find_pic_touch(rd.cloud_submit)
        # # 点击棋盘后切换页面
        # if(gamer.verify_pic(rd.back_from_board)):
        #     print("在设备{0}中，已经进入棋盘".format(gamer.deviceID))
        #     break
        # TODO 云端数据切换
        if(gamer.find_pic_touch(rd.into_board)): 
            print("在设备{0}中，点击进入棋盘".format(gamer.deviceID))
            time.sleep(1)
            break

    # 备用机返回主页
    gamer.bs_press('1')

def save_main_device():
    gamer.deviceID = deviceID
    if (not gamer.init_window_save(windowID)): raise Exception(f'切换页面失败, 未能定位到窗口: {windowID}')
    gamer.bs_press('1')
    time.sleep(3)  # 等待窗口激活
    gamer.find_pic_touch(rd.start_game)
    time.sleep(5)  # 等待窗口激活
    # while True:
    #     time.sleep(0.5)  # 等待窗口激活
    #     if(gamer.verify_pic(rd.init_loading)):
    #         print("在设备{0}中，成功重新保存".format(gamer.deviceID))

def resume_main_device(waitSeconds = 3):
    # 新的启动流程流程
    gamer.deviceID = deviceID
    if (not gamer.init_window_save(windowID)): raise Exception(f'切换页面失败, 未能定位到窗口: {windowID}')

    gamer.bs_press('1')
    time.sleep(waitSeconds)  # 等待窗口激活
    gamer.find_pic_touch(rd.start_game)
    while True:
        time.sleep(0.5)  # 等待窗口激活
        if(gamer.verify_pic(rd.cloud_button)):
            time.sleep(3)  # 等待云端数据可选
            gamer.find_pic_touch(rd.cloud_button)
            time.sleep(5)  # 等待云端数据可选
            gamer.find_pic_touch(rd.cloud_submit)
        # 点击棋盘后切换页面
        # if(gamer.verify_pic(rd.back_from_board)):
        #     print("在设备{0}中，已经进入棋盘".format(gamer.deviceID))
        #     break
        # TODO 云端数据切换
        if(gamer.find_pic_touch(rd.into_board)): 
            print("在设备{0}中，点击进入棋盘".format(gamer.deviceID))
            time.sleep(1)
            break

def select_box():
    time.sleep(2)
    # 首先选中箱子
    if not gamer.verify_pic(rd.box_2):
        gamer.find_pic_touch(rd.box_1)
        time.sleep(1)



# [脚本从这里开始运行]
reset_sub_device()
resume_main_device()
select_box()

count = len(gamer.find_pic_all(rd.power_4))
countNow = count

# 获取箱子初始数量
boxList = gamer.find_pic_all(rd.box_1)
boxCount = len(boxList)
point = (0,0)
if len(boxList) > 0:
    point = boxList[0]
else:
    raise Exception(f'箱子列表为空')

# 更新箱子列表
boxList = gamer.find_pic_all(rd.box_1)
if len(boxList) < boxCount:
    boxCount = len(boxList)
    if len(boxList) > 0:
        point = boxList[0]
    else:
        raise Exception(f'箱子列表为空')
# 选中箱子
if not gamer.verify_pic(rd.box_2):
    gamer.touch(point)

# 点击箱子
time.sleep(0.5)
gamer.touch(point)

# while gamer.find_pic_touch(rd.box_selected):
while gamer.find_pic_touch(rd.box_selected):
    print("在设备{0}中，点击体力箱".format(gamer.deviceID))
    time.sleep(1.5)
    powerList = gamer.find_pic_all(rd.power_4)
    countNow = len(powerList)
    print("在设备{0}中，获取4级体力瓶个数: {1}".format(gamer.deviceID, countNow))
    if countNow > count:
        if countNow > 1:
            # 合成
            gamer.slide((powerList[0], powerList[1]))
            time.sleep(1.5)
            if not gamer.verify_pic(rd.box_2):
                gamer.find_pic_touch(rd.box_1)
        # 保存并重置体力瓶数量
        count = len(gamer.find_pic_all(rd.power_4))
        print("在设备{0}中，合成后4级体力瓶个数: {1}".format(gamer.deviceID, count))
        save_main_device()
        select_box()
    else :
        # 舍弃现有结果
        gamer.bs_press('1')
        # 次设备重置结果
        reset_sub_device()
        resume_main_device(0.5)
        select_box()

# TODO main_device其他操作
