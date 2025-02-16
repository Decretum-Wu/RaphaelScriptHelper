import RaphaelScriptHelper as gamer
import multiprocessing
import testDict as rd
import settings
import pyautogui
import time
import ADBHelper
import logging
import GhHelper as ghh
import ImageProc
import GhOrange as gho
import GhEventHelper as gheh
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
# deviceID = "127.0.0.1:5625"
# deviceID2 = "127.0.0.1:5625"
# deviceID = "emulator-5584"
# deviceID2 = "127.0.0.1:5595"
manager_pos_1 = (900, 225)
manager_pos_2 = (900, 330)
manager_pos_submit = (900, 600)
retryNum = 5
doneFlag = False
cardMaxX = 180
cardMaxY = 70
#cardMinX = 0

gamer.deviceID = deviceID
# gamer.home()
# powerList = gamer.debug_find_pic_all(rd.power_4)
# countNow = len(powerList)
# print("在设备{0}中，获取目标个数: {1}".format(gamer.deviceID, countNow))

targetListCoin = [
    rd.coin_0,
    rd.coin_new_1,
    rd.coin_new_2,
    rd.coin_new_3,
    rd.coin_new_4
]

targetListGift = [
    rd.event_gift_1_new,
    rd.event_gift_2,
    rd.event_gift_3,
    rd.event_gift_4,
    rd.event_gift_5,
    rd.event_gift_6,
    rd.event_gift_7,
    rd.event_gift_8
]

targetListPower = [
    rd.power_1_new,
    rd.power_2_new,
    rd.power_3,
    rd.power_4
]

targetListBear = [
    rd.event_bear_2,
    rd.event_bear_3,
    rd.event_bear_4,
]

targetListOrange = [
    rd.orange_1_a,
    rd.orange_2_a,
    rd.orange_3_a,
    rd.orange_4_a,
    rd.orange_5_a,
    rd.orange_6_a
]

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

def count_resource(target):
    return len(ghh.stable_find_board_items(target, retryNum))

def find_first_resource_point(target, remainNum = 0):
    resourceList = ghh.stable_find_board_items(target, retryNum)
    logging.info("find_first_resource_point for {0} get number {1}, when remainNum {2}".format(target, len(resourceList), remainNum))
    if len(resourceList) > remainNum:
        return resourceList[0]
    else:
        return False

def simple_merge(target):
    current_list = ghh.stable_find_board_items(target, retryNum)
    logging.info("simple_merge for {0} get number {1}".format(target, len(current_list)))
    # 跳过无效列表记录
    if len(current_list) < 2:
        status = "empty" if not current_list else "single-element"
        logging.info(f"simple_merge ({status}) skipped")

    merged_results = []
    # 持续处理直到剩余元素不足两个
    while len(current_list) >= 2:
        # 总是取出前两个元素
        a = current_list.pop(0)
        b = current_list.pop(0)
        merged_results.append(gamer.slide(a, b))
        # 实时日志
        logging.debug(f"Merged ({a}, {b}) for target {target}")

# # 刷卡包调试
# while not gamer.find_pic_touch(rd.card_4_bag):
#     #done
#     print(f"retry touch")

# time.sleep(3)
# # 打开卡包TODO,点击固定点 
# gamer.find_pic_touch(rd.card_1)
# time.sleep(3)
# # 验证新卡
# if gamer.verify_pic(rd.card_new):
#     cardCollection = gamer.find_pic_all_list([
#             rd.card_star_4,
#             rd.card_new
#         ], 0.8)

#     if len(cardCollection[0]) == 0:
#         print(f"error")
#         raise Exception(f'错误：未能获取高级卡包位置')
#     topCardPoint = cardCollection[0][0]

#     # if len(cardCollection[0]) == 0:
#     #     print(f"提示：未能获取新卡")
#     x, y = topCardPoint
#     for point in cardCollection[1]:
#         ex, ey = point
#         if ex-x > 0 and ex-x < cardMaxX and ey-y > 0 and ey-y < cardMaxY:
#             doneFlag = True
#             print(f"提示：成功获取新卡")
#             # save and break 2 times
#     # 若未成功
#     if not doneFlag:
#         print(f"提示：未能获取新卡")
#         # break and resume
#     else:
#         doneFlag = False
#         #continue
# else:
#     print(f"提示：未能获取新卡")
#     # break and resume

# 新调试：
# try:
#     gamer.collect_log_image()
# except Exception as e:
#     print(f"捕获异常: {e}")

# gamer.bs_manager_click(windowID3, manager_pos_1)

# ghh.click_order(rd.order_orange)

# temp = ImageProc.get_color(rd.empty_brown_1,(64,64))
# print("在设备{0}中，获取目标个数: {1}".format(gamer.deviceID, powerCol[0]))
# temp = gamer.find_all_empty(ghh.get_all_center())

# temp = 0
# while not gho.leave_incident_with_normal_flag():
#     temp += 1

# temp = gho.verify_empty()
# temp = len(gheh.get_all_center())

# powerCol = gamer.find_pic_all_list(targetListBear)
# powerCol = gheh.get_collection_unique_grid_positions(powerCol)

treeCol = gamer.find_pic_all_list([
            rd.orange_tree_new
        ])
treeCol = ghh.get_collection_unique_grid_positions(treeCol)

# powerCol = gamer.find_pic_all_list(targetListOrange)
print("在设备{0}中，获取橘子树总数: {1}".format(gamer.deviceID, len(treeCol[0])))
# print("temp:{0}".format(powerCol))

