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
import GhEventHelper_2 as gheh2
import subprocess
from enum import Enum
import GhTempTest as gtest

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

windowID = "BlueStacks App Main"
windowID2 = "BlueStacks App Player 2"
windowID3 = "BlueStacks Multi"
deviceID = settings.deviceList[0]["deviceId"]
deviceID2 = settings.deviceList[1]["deviceId"]

manager_pos_1 = (900, 225)
manager_pos_2 = (900, 330)
manager_pos_submit = (900, 600)
retryNum = 5
doneFlag = False
cardMaxX = 180
cardMaxY = 70
stayFlag = True

settings.accuracy = 0.85
targetStartNum = 0
#正确率0.55时，bubble难以判断
#正确率0.6时，为最佳经验值

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

targetListOrange = [
    rd.orange_1_stable,
    rd.orange_2_stable,
    rd.orange_3_stable,
    rd.orange_4_stable,
    rd.orange_5_stable,
    rd.orange_6_stable
]

targetListStone = [
    rd.stone_0,
    rd.stone_1,
    rd.stone_2,
    rd.stone_3
]

def restart_all():
    # 重置跳过变量，重启后必须重新进入游戏
    global stayFlag
    stayFlag = False
    # 首次点击容易失败，重复点击更安全
    gamer.stop_process_by_window_title(settings.deviceList[0]["window_title"])
    gamer.stop_process_by_window_title(settings.deviceList[1]["window_title"])
    gamer.delay(25)
    gamer.run_bluestacks_instance(settings.deviceList[0]["instance_title"])
    gamer.run_bluestacks_instance(settings.deviceList[1]["instance_title"])
    gamer.delay(35)
    ADBHelper.connent(settings.deviceList[0]["deviceId"])
    ADBHelper.connent(settings.deviceList[1]["deviceId"])
    gamer.delay(5)

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

# def stop_process_by_window_title(window_title):
#     # PowerShell命令模板
#     ps_command = '''
#     Get-Process | Where-Object {{ $_.MainWindowTitle -eq "{0}" }} | Stop-Process -Force
#     '''.format(window_title)

#     # 使用subprocess运行PowerShell命令
#     result = subprocess.run(["powershell", "-Command", ps_command], capture_output=True, text=True)

#     # 输出结果
#     if result.returncode == 0:
#         print(f"成功终止窗口标题为 '{window_title}' 的进程。")
#     else:
#         print(f"未能终止窗口标题为 '{window_title}' 的进程。错误信息：")
#         print(result.stderr)


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

# def get_all_center():
#     resultList = []
#     for col in range(7,8):
#         for row in range(7,9):
#             x = 64 + (col - 1) * 136 + 68  # 计算x坐标：起点64 + (列数-1)*格子宽度 + 半宽
#             y = 508 + (row - 1) * 136 + 68  # 计算y坐标：起点508 + (行数-1)*格子高度 + 半高
#             resultList.append((x,y))
#     return resultList

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

# 橘子树

# treeCol = gamer.find_pic_all_list_cache([
#             rd.orange_tree_new
#         ])
# treeCol = ghh.get_collection_unique_grid_positions(treeCol)
# print("在设备{0}中，获取橘子树总数: {1}".format(gamer.deviceID, len(treeCol[0])))

# powerCol = ghh.get_collection_unique_grid_positions_read(gamer.find_pic_all_list_cache(targetListOrange))
# # powerCol = gamer.find_pic_all_list(targetListOrange)
# powerCol = ghh.read_list_to_unique_grid_positions()

# 固定列表橘子树
# for tree in rd.orange_tree_list2:
#     gamer.touch(tree)
#     gamer.delay(1)

# gamer.collect_log_image()

# print("temp:{0}".format(get_all_center()))
# [(268, 576), (268, 712), (268, 848), (268, 984), (268, 1120), (268, 1256), (268, 1392), (268, 1528), (948, 1392), (948, 1528)]


# 环境变量
# targetList = [
#     {"deviceId": 'emulator-5554', "window_title": 'BlueStacks App Main', "instance_title": 'Pie64'},
#     {"deviceId": '127.0.0.1:5635', "window_title": 'BlueStacks App Save2', "instance_title": 'Pie64_8'},
#     {"deviceId": '127.0.0.1:5585', "window_title": 'BlueStacks App Sub Main', "instance_title": 'Pie64_3'},
#     {"deviceId": '127.0.0.1:5615', "window_title": 'BlueStacks App Sub Save', "instance_title": 'Pie64_6'},
# ]

# deviceID = "emulator-5554"
# deviceID2 = "127.0.0.1:5625"

# # deviceID = "127.0.0.1:5585"
# # deviceID2 = "127.0.0.1:5615"
# # 示例调用
# window_title = "BlueStacks App Save2"  # 替换为传入的参数
# instance_title = "Nougat64_4"
# i = 0
# gamer.stop_process_by_window_title(targetList[i]["window_title"])
# time.sleep(10)
# gamer.run_bluestacks_instance(targetList[i]["instance_title"])
# time.sleep(30)


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

targetListCoin = [
    rd.coin_0,
    rd.coin_new_1,
    rd.coin_new_2,
    rd.coin_new_3,
    rd.coin_new_4
]

targetListItem = [
    rd.event_2_item_1,
    rd.event_2_item_2,
    rd.event_2_item_3,
    rd.event_2_item_4,
    rd.event_2_item_5,
    rd.event_2_item_6,
    rd.event_2_item_7,
]

targetListTag = [
    rd.event_2_tag_1,
    rd.event_2_tag_2,
]

targetListItem = [
    rd.ring_item_3,
    rd.ring_item_4,
    rd.ring_item_6,
]

# 测试，连接
ADBHelper.connent(settings.deviceList[0]["deviceId"])
ADBHelper.connent(settings.deviceList[1]["deviceId"])

# targetListPower = [
#     rd.power_1_new,
#     rd.power_2_new,
#     rd.power_3,
#     rd.power_4
# ]

# targetListTemp = settings.eventTagList

# 测试新列表
# targetListTemp = targetListItem

# temp = ghh.get_collection_unique_grid_positions_read(gamer.find_pic_all_list(targetListTemp, 0.65))

# # temp = ghh.calculate_total_weight(temp)
# print("temp:{0}".format(temp))


# temp = ghh.get_center((1,5))
# temp = ghh.get_all_center()
# temp = gamer.find_all_empty(ghh.get_all_center())
# temp = gamer.find_all_color([ghh.get_center((8,3))])
# i = 0
# for i in range(1,997):
#     gamer.touch((891, 795))
#     gamer.delay(0.1)

# # temp = i

# temp = gtest.game_start_clean()

# temp = gheh.get_collection_unique_grid_positions_read(gamer.find_pic_all_list(targetListTemp, 0.75))
# print("temp:{0}".format(temp))

# restart_all()
# for i in range(1,20):
#     temp = gamer.find_pic(rd.card_5, True, 0.7, False)


#活动列表

targetList = [
    {"targetItem": rd.event_4_a_tag_1, "targetAcc":0.85, "mergeRequired": True},
    # {"targetItem": settings.eventTagList[0], "targetAcc":0.85, "mergeRequired": True},
]
currentTarget = targetList[targetStartNum]

# count = gheh.stable_find_board_items_read(currentTarget["targetItem"], 2, 0.75)
# print("temp:{0}".format(count))

# temp = gheh.get_collection_unique_grid_positions_read(gamer.find_pic_all_list(settings.eventTagList, 0.75))
# targetListStone
temp = gheh.get_collection_unique_grid_positions_read(gamer.find_pic_all_list(targetListStone, 0.75))
print("temp:{0}".format(temp))