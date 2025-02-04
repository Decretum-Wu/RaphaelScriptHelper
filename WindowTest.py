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
windowID3 = "BlueStacks Multi"
deviceID = "emulator-5554"
deviceID2 = "emulator-5574"
manager_pos_1 = (900, 225)
manager_pos_2 = (900, 330)
manager_pos_submit = (900, 600)
# gamer.deviceID = "emulator-5554"

def restart_all():
    gamer.bs_manager_click(windowID3, manager_pos_1)
    gamer.delay(1)
    gamer.bs_manager_click(windowID3, manager_pos_submit)
    gamer.delay(1)
    gamer.bs_manager_click(windowID3, manager_pos_2)
    gamer.delay(1)
    gamer.bs_manager_click(windowID3, manager_pos_submit)
    gamer.delay(20)
    gamer.bs_manager_click(windowID3, manager_pos_1)
    gamer.delay(5)
    gamer.bs_manager_click(windowID3, manager_pos_2)
    gamer.delay(10)

# 完整刷新流程
def reset_sub_device():
    gamer.deviceID = deviceID2
    # if (not gamer.init_window_save(windowID2)): raise Exception(f'切换页面失败, 未能定位到窗口: {windowID2}')
    # # bs_press h-断网 1-返回主页
    # gamer.bs_press('1')
    gamer.home()
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
        # time.sleep(0.5)  # 等待窗口激活
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
        if(gamer.find_pic_touch(rd.start_game)):
            continue

    # 备用机返回主页
    gamer.home()

def save_main_device():
    gamer.deviceID = deviceID
    gamer.home()
    time.sleep(3)  # 等待窗口激活
    gamer.find_pic_touch(rd.start_game)
    time.sleep(2)  # 等待窗口激活
    # while True:
    #     time.sleep(0.5)  # 等待窗口激活
    #     if(gamer.verify_pic(rd.init_loading)):
    #         print("在设备{0}中，成功重新保存".format(gamer.deviceID))

def resume_main_device(waitSeconds = 3):
    # 新的启动流程流程
    gamer.deviceID = deviceID
    gamer.home()
    time.sleep(1)  # 等待窗口激活
    gamer.find_pic_touch(rd.start_game)
    time.sleep(waitSeconds)  # 等待窗口激活
    while True:
        # time.sleep(0.5)  # 等待窗口激活
        if(gamer.verify_pic(rd.cloud_button)):
            time.sleep(3)  # 等待云端数据可选
            gamer.find_pic_touch(rd.cloud_button)
            time.sleep(3)  # 等待云端数据可选
            gamer.find_pic_touch(rd.cloud_submit)
        # 点击棋盘后切换页面
        # if(gamer.verify_pic(rd.back_from_board)):
        #     print("在设备{0}中，已经进入棋盘".format(gamer.deviceID))
        #     break
        # TODO 云端数据切换
        if(gamer.find_pic_touch(rd.into_board)): 
            print("在设备{0}中，点击进入棋盘".format(gamer.deviceID))
            time.sleep(5)
            break
        if(gamer.find_pic_touch(rd.start_game)):
            continue

# [脚本从这里开始运行]
reset_sub_device()
resume_main_device()

# 防止体力瓶初值错误
time.sleep(2.5)
count = len(gamer.find_pic_all(rd.power_4))
if count == 0:
    time.sleep(5)
    count = len(gamer.find_pic_all(rd.power_4))
countNow = count
print("在设备{0}中，初始4级体力瓶个数: {1}".format(gamer.deviceID, countNow))

# 获取箱子初始数量
point = (0,0)
boxList = gamer.find_pic_all(rd.box_1)
boxCount = len(boxList)
if len(boxList) > 0:
    point = boxList[0]
else:
    raise Exception(f'箱子列表为空')
errorCount = 0

roundCount = 0

# while gamer.find_pic_touch(rd.box_selected):
while True:
    # 更新箱子列表
    boxList = gamer.find_pic_all(rd.box_1)
    if len(boxList) < boxCount:
        if len(boxList) > 0:
            point = boxList[0]
            boxCount = len(boxList)
        else:
            errorCount += 1
            print("在设备{0}中，体力箱为0，重新判断")
            if errorCount > 10:
                break
                # raise Exception(f'箱子列表为空')
            continue
            
    # 选中箱子
    if not gamer.verify_pic(rd.box_2):
        gamer.touch(point)
        time.sleep(0.5)

    # 点击箱子
    gamer.touch(point)

    print("在设备{0}中，点击体力箱".format(gamer.deviceID))
    time.sleep(1.5)
    powerList = gamer.find_pic_all(rd.power_4)
    countNow = len(powerList)
    roundCount += 1
    print("在设备{0}中，获取4级体力瓶个数: {1}".format(gamer.deviceID, countNow))
    if roundCount % 5 == 0:
        tempList = gamer.find_pic_all_list([rd.power_2, rd.power_4])
        logging.info(msh.send_simple_push("在第{0}次执行中，获取体力瓶列表: {1}".format(roundCount, tempList),"提示：完成一轮刷新"))
    if countNow > count:
        if countNow > 1:
            # 合成
            gamer.slide(powerList[0], powerList[1])
            time.sleep(1.5)
        # 保存并重置体力瓶数量
        count = len(gamer.find_pic_all(rd.power_4))
        print("在设备{0}中，合成后4级体力瓶个数: {1}".format(gamer.deviceID, count))
        save_main_device()
        logging.info(msh.send_simple_push("1","提示：获得一个四级瓶"))
        logging.info("获得一个四级瓶")
    else :
        if roundCount % 10 == 0:
            restart_all()
        # 舍弃现有结果
        gamer.home()
        # 次设备重置结果
        reset_sub_device()
        resume_main_device(0.5)
        # 重置错误次数
        errorCount = 0
logging.info(msh.send_simple_push("箱子列表为空","提示：完成一轮执行"))
logging.info("完成执行")