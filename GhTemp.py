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
import GhOrange as gho
import ADBHelper
import datetime
from enum import Enum

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
targetListBeike = [
    rd.beike_3,
    rd.beike_4,
    rd.beike_5_1,
    rd.beike_6,
    rd.beike_7,
    rd.beike_8,
    rd.beike_9,
    rd.beike_10
]

checkPower = 190

targetListFish = [
    rd.fish_item_1,
    rd.fish_item_2,
    rd.fish_item_3,
    rd.fish_item_4,
    rd.fish_item_5,
    rd.fish_item_6,
    rd.fish_item_7,
    rd.fish_item_8,
]

targetListBread = [
    rd.bread_3,
    rd.bread_4,
    rd.bread_5,
    rd.bread_6,
    rd.bread_7,
    rd.bread_8,
    rd.bread_9,
    rd.bread_10
]

targetListBreadTag = [
    rd.bread_tag_3,
    rd.bread_tag_4,
    rd.bread_tag_5,
    rd.bread_tag_6,
    # rd.bread_tag_7
]
intoGameList = [
    rd.start_game,
    rd.cloud_button,
    rd.into_board,
    rd.back_from_board
    ]
windowID3 = "BlueStacks Multi"
deviceID = settings.deviceList[0]["deviceId"]
deviceID2 = settings.deviceList[1]["deviceId"]
managerPos1 = (900, 220)
managerPos2 = (900, 330)
managerPosSubmit = (900, 600)
gamer.deviceID = deviceID
errorCount = 0
roundCount = 1
refreshCount = 1
tagCount = 0
point = (0,0)
stayFlag = False
switchFlag = False
retryNum = 3
retryNumMin = 2
resourceAcc = 0.55
targetAcc = 0.55
settings.accuracy = 0.70
# startAtOrange = False
# startAtOrange = True

# resourceItem = rd.daily_box_3
# targetItem = rd.power_3
# mergeRequired = True
# 重要
gho.useCoin = True
gho.usePower = False
# gho.useCoin = True
# gho.usePower = True
# startAtOrange = 0
refreshCount = 0
# card_1 = 2
# daily_box_3 = 4
targetStartNum = 2
targetCount = 2

# 1 刷卡片
cardFlag = False
bagStep = 3
bagTop = rd.card_4_bag
# bagTagList = [rd.card_star_4, rd.card_star_5]
bagTagList = []

# 2 刷新完物品后继续刷体力
roundFlag = False

# 3 刷箱子
getBoxFlag = True
# 4 刷物品
getBoxFlag = False
exitFlag = False
# 物品未获取时保留图片
collectImg = True
# 体力目标
tagAcc = 0.55
itemImg = False

# 贝壳
tagListTag = []
itemPoint = ghh.get_center((1,4))
tagList = targetListBeike
tagAcc = 0.65
stepLen = 1
targetWeight = 2
lastWeight = 1191

startPower = 126
tagNum = 0
# 128为10级
# 单次直接刷2非常难，几乎不可能

# # 面包
# tagListTag = targetListBreadTag
# itemPoint = ghh.get_center((1,3))
# tagList = targetListBread
# tagAcc = 0.70
# stepLen = 1
# targetWeight = 2
# lastWeight = 1300

# 鱼(原始)
# itemPoint = ghh.get_center((7,1))
# tagList =[rd.fish_source_3, rd.fish_resource_4, rd.fish_source_5]
# stepLen = 1
# targetWeight = 2
# lastWeight = 27

# 鱼(产物)
# itemPoint = ()
# itemImg = rd.fish_source_5
# tagList = targetListFish
# # (产物)12次，需为约数方能避免点击空格
# stepLen = 3
# targetWeight = 4
# lastWeight = 300

targetList = [
    {"resourceItem": rd.card_1, "resourceAcc":0.55, "targetItem": rd.stone_4, "targetAcc":0.50, "mergeRequired": False, "consumeItem": rd.stone_4},
        {"resourceItem": rd.coin_box, "resourceAcc":0.55, "targetItem": rd.coin_new_4, "targetAcc":0.75, "mergeRequired": True, "consumeItem": rd.coin_new_5},
    # {"resourceItem": rd.licence_box_3_max, "resourceAcc":0.55, "targetItem": rd.stone_4, "targetAcc":0.55, "mergeRequired": False, "consumeItem": rd.stone_4},
    # {"resourceItem": rd.resource_blank, "resourceAcc":0.65, "targetItem": rd.coffee_tag_3, "targetItem2": rd.beard_tag_3,"targetAcc":0.65, "mergeRequired": True},
    #  {"resourceItem": rd.license_box_1, "resourceAcc":0.55, "targetItem": rd.stone_3, "targetAcc":0.55, "mergeRequired": False, "consumeItem": rd.stone_4},
        {"resourceItem": rd.box_1, "resourceAcc":0.6, "targetItem": rd.power_4, "targetAcc":0.75, "mergeRequired": True},#, "consumeItem": rd.power_5},
    # {"resourceItem": rd.box_1, "resourceAcc":0.6, "targetItem": rd.power_4, "targetAcc":0.75, "mergeRequired": True, "consumeItem": rd.power_5},
        # {"resourceItem": rd.coin_box, "resourceAcc":0.55, "targetItem": rd.coin_new_4, "targetAcc":0.75, "mergeRequired": True},#, "consumeItem": rd.coin_new_5},
            # {"resourceItem": rd.license_box_2_1, "resourceAcc":0.55, "targetItem": rd.stone_3, "targetAcc":0.75, "mergeRequired": True},
                   {"resourceItem": rd.daily_box_3, "resourceAcc":0.55, "targetItem": rd.power_3, "targetItem2": rd.coin_new_3, "targetAcc":0.75,"mergeRequired": True, "consumeItem": rd.coin_new_5},
    # {"resourceItem": rd.daily_box_3, "resourceAcc":0.55, "targetItem": rd.power_3, "targetAcc":0.75,"mergeRequired": True},
    # {"resourceItem": rd.box_1, "resourceAcc":0.6, "targetItem": rd.power_4, "targetAcc":0.75, "mergeRequired": True},#, "consumeItem": rd.power_5},
]
# "targetAcc":0.55 在无订单时容易误判，可以用0.65
    # {"resourceItem": rd.resource_blank, "resourceAcc":0.65, "targetItem": rd.coffee_tag_3, "targetItem2": rd.beard_tag_3,"targetAcc":0.55, "mergeRequired": True},

# targetList = [
#     {"resourceItem": rd.resource_blank, "resourceAcc":0.65, "targetItem": rd.coffee_tag_3, "targetAcc":0.55, "mergeRequired": True},
#     {"resourceItem": rd.resource_blank, "resourceAcc":0.65, "targetItem": rd.coffee_tag_3, "targetItem2": rd.beard_tag_3,"targetAcc":0.55, "mergeRequired": True},
#     # {"resourceItem": rd.box_1, "resourceAcc":0.6, "targetItem": rd.power_4, "targetAcc":0.75, "mergeRequired": True},
#     # {"resourceItem": rd.daily_box_3, "resourceAcc":0.55, "targetItem": rd.power_3,  "targetAcc":0.75,"mergeRequired": True},
# ]

# targetList = [
#     {"resourceItem": rd.license_box_1, "resourceAcc":0.55, "targetItem": rd.stone_3, "targetAcc":0.75, "mergeRequired": True},
#     {"resourceItem": rd.license_box_2_1, "resourceAcc":0.55, "targetItem": rd.stone_3, "targetAcc":0.75, "mergeRequired": True},
#     {"resourceItem": rd.license_box_3, "resourceAcc":0.55, "targetItem": rd.blue_resource_1, "targetAcc":0.55, "mergeRequired": True},
#     # {"resourceItem": rd.licence_box_3_max, "resourceAcc":0.55, "targetItem": rd.stone_4, "targetAcc":0.55, "mergeRequired": False, "consumeItem": rd.stone_4},
# ]
currentTarget = targetList[targetStartNum]

def into_game(verifyIntoFlag = False):
    continueFlag = True
    doneIntoFlag = False
    retryCount = 0
    gamer.home()
    while continueFlag:
        totalList = gamer.find_pic_all_list(intoGameList)
        totalDict = ghh.combine_lists_to_dict(intoGameList, totalList)
        for key in intoGameList:
            if len(totalDict[key]) > 0:
                match key:
                    # cloud_button
                    case rd.cloud_button: 
                        time.sleep(3)  # 等待云端数据可选
                        gamer.find_pic_touch(rd.cloud_button)
                        time.sleep(5)  # 等待云端数据可选
                        gamer.find_pic_touch(rd.cloud_submit)
                        time.sleep(3)
                        break
                    # 进入棋盘后无需额外操作
                    case rd.into_board: 
                        gamer.touch(totalDict[key][0])
                        # 如果不需要确认已进入，则直接跳出，否则依赖back_from_board跳出
                        if not verifyIntoFlag:
                            continueFlag = False
                        else:
                            #防止截图过快导致的后续问题
                            doneIntoFlag = True
                            time.sleep(2)
                        break
                    # back_from_board
                    case rd.back_from_board: 
                        if doneIntoFlag:
                            logging.info(f"已点击进入棋盘，跳过额外验证")
                            continueFlag = False
                            break
                        elif verifyIntoFlag:
                            time.sleep(15)
                        else:
                            time.sleep(15)
                        # 始终未刷新，可能已经自动保存，则不做处理
                        if(gamer.verify_pic(rd.back_from_board)):
                            logging.info(f"正常刷新，5秒后依旧在棋盘内")
                            continueFlag = False
                            break
                        else:
                            time.sleep(5)
                            if(gamer.verify_pic(rd.back_from_board)):
                                logging.info(f"异常刷新，但10秒后依旧在棋盘内，已解决")
                                continueFlag = False
                                break
                            # 重新尝试整个刷新逻辑
                            break
                    # 其他操作，需要等待结果
                    case _:
                        # retryCount = 0
                        gamer.touch(totalDict[key][0])
                        time.sleep(5)
                        break
        # 一轮识别后的处理
        retryCount += 1
        if retryCount % 60 == 0 and continueFlag:
            # 30次尝试一次解决卡顿
            msh.send_simple_push(f"retryCount 为{retryCount}","错误：已经卡死,试图解决卡顿")
            gamer.touch(rd.first_screen_close_1)
            time.sleep(1)
            gamer.touch(rd.first_screen_close_2)
            time.sleep(5)
            if gamer.verify_pic(rd.into_board):
                msh.send_simple_push(f"retryCount 为{retryCount}","成功：成功解决卡顿")
                # 首屏问题一般为礼包，关闭后需要保存
                gamer.home()
                time.sleep(3)  # 等待窗口激活
                gamer.find_pic_touch(rd.start_game)
                time.sleep(5)  # 等待窗口激活
            else:
                msh.send_simple_push(f"retryCount 为{retryCount}","错误：卡顿未能解决，尝试重启")
                gamer.collect_log_image()
                raise Exception(f'错误：卡顿未能解决，尝试重启，retryCount 为{retryCount}')

def switch_device():
    if(gamer.deviceID == deviceID2): gamer.deviceID = deviceID
    else: gamer.deviceID = deviceID2
    logging.info(f"切换至设备{gamer.deviceID}")

def restart_all():
    # 重置跳过变量，重启后必须重新进入游戏
    global stayFlag
    stayFlag = False
    # 首次点击容易失败，重复点击更安全
    gamer.stop_process_by_window_title(settings.deviceList[0]["window_title"])
    gamer.stop_process_by_window_title(settings.deviceList[1]["window_title"])
    gamer.delay(15)
    gamer.run_bluestacks_instance(settings.deviceList[0]["instance_title"])
    gamer.delay(15)
    gamer.run_bluestacks_instance(settings.deviceList[1]["instance_title"])
    gamer.delay(20)
    ADBHelper.connent(settings.deviceList[0]["deviceId"])
    ADBHelper.connent(settings.deviceList[1]["deviceId"])
    gamer.delay(5)
    

# 完整刷新流程
def reset_sub_device():
    gamer.deviceID = deviceID2
    # if (not gamer.init_window_save(windowID2)): raise Exception(f'切换页面失败, 未能定位到窗口: {windowID2}')
    # # bs_press h-断网 1-返回主页
    # gamer.bs_press('1')
    gamer.home()
    time.sleep(0.5)
    gamer.find_pic_touch(rd.start_game)
    into_game()
    # 备用机返回主页
    gamer.home()

def save_current_device():
    gamer.home()
    time.sleep(3)  # 等待窗口激活
    gamer.find_pic_touch(rd.start_game)
    time.sleep(5)  # 等待窗口激活

def count_resource(target):
    return len(ghh.stable_find_board_items(target, retryNum, resourceAcc))

def find_first_resource_point(target, remainNum = 0):
    resourceList = ghh.stable_find_board_items(target, retryNum, resourceAcc)
    logging.info("find_first_resource_point for {0} get number {1}, when remainNum {2}".format(target, len(resourceList), remainNum))
    if len(resourceList) > remainNum:
        return resourceList[0]
    else:
        return False

def simple_merge(target, acc):
    current_list = ghh.stable_find_board_items(target, retryNum, acc)
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

def set_acc_by_item(currentTarget):
    global resourceAcc, targetAcc
    if currentTarget.get("resourceAcc"): resourceAcc = currentTarget.get("resourceAcc")
    if currentTarget.get("targetAcc"): targetAcc = currentTarget.get("targetAcc")

def check_card_result(bagTagList = [rd.card_star_4, rd.card_star_5]):
    # 验证新卡
    doneFlag = False
    countCard = 0
    tagLen = len(bagTagList)
    tagPointList = []
    bagTagList.append(rd.card_new)
    if gamer.verify_pic(rd.card_new):
        # tagLen == 0，即接受任意新卡
        if tagLen == 0:
            doneFlag = True
            print(f"提示：成功获取新卡, 任意")
        else:
            cardCollection = gamer.find_pic_all_list(bagTagList, 0.8)
            for i in range(0,tagLen):
                countCard += len(cardCollection[i])
                if len(cardCollection[i]) > 0:
                    tagPointList.append(cardCollection[i][0])
            if countCard == 0:
                print(f'错误：未能获取高级卡包位置')
                raise Exception(f'错误：未能获取高级卡包位置')
            
            # if len(cardCollection[0]) == 0:
            #     print(f"提示：未能获取新卡")

            # topCardPoint = cardCollection[0][0]

            for topCardPoint in tagPointList:
                x, y = topCardPoint
                for point in cardCollection[tagLen]:
                    ex, ey = point
                    if ex-x > 0 and ex-x < settings.cardMaxX and ey-y > 0 and ey-y < settings.cardMaxY:
                        doneFlag = True
                        print(f"提示：成功获取新卡")

        # 若未成功
        if not doneFlag:
            print(f"提示：未能获取新卡")
            # break and resume
        else:
            print(f"提示：成功获取新卡,待保存")
            # save and coutinue
    else:
        print(f"提示：未能获取新卡")
        doneFlag = False
    return doneFlag

def get_card(bagStep = 1, bagTop = rd.card_5, bagTagList = [rd.card_star_4, rd.card_star_5]):
    point = ()
    doneFlag = False
    pos1, pos2 = rd.slide_to_card
    gamer.slide(pos1, pos2)
    gamer.delay(1.5)
    point = gamer.find_pic(bagTop, True, 0.7, False)
    if not point:
        gamer.slide(pos1, pos2)
        gamer.delay(1.5)
    point = gamer.find_pic(bagTop, True, 0.6, False)
    if point:
        for i in range(0, bagStep):
            gamer.touch(point)
            gamer.delay(1)
            gamer.touch(settings.empty_block)
            gamer.delay(3)
            # 验证新卡
            if check_card_result(bagTagList):
                doneFlag = True
                print(f"提示：成功获取新卡")
                break
            elif i < bagStep -1:
                # 如果失败且还有卡包，重新点击下个卡包
                gamer.touch(settings.empty_block)
                gamer.delay(3)
    else:
        logging.error(f"出现问题,找不到卡包")
        # gamer.delay(3600)
        msh.send_simple_push(f"错误内容",f"提示：出现问题,找不到卡包")
        raise Exception(f'出现问题,找不到卡包')
    return doneFlag

def get_cards(targetCount = 1, collectImg = True):
    global stayFlag, switchFlag, currentTarget, targetList, exitFlag, roundFlag
    global bagStep, bagTop, bagTagList
    tagCount = 0
    roundCount = 1
    errorCount = 0
    refreshCount = 0
    ADBHelper.connent(deviceID)
    ADBHelper.connent(deviceID2)

    if gho.verify_empty():
        logging.info("测试：目前有空位")
    while True:
        if tagCount >= targetCount:
            break
        if gho.verify_exit():
            exitFlag = True
            break
        try:
            if not stayFlag:
                into_game(True)
            else:
                stayFlag = False

            if len(ADBHelper.getDevicesList()) < 2:
                logging.info(msh.send_simple_push("目标列表为空","提示：重启出现问题，尝试恢复"))
                errorCount += 1
                if errorCount < 3:
                    msh.send_simple_push(f"开始重启,错误次数{errorCount}",f"提示：执行{roundCount}次卡死，开始重启")
                    restart_all()
                    msh.send_simple_push(f"完成重启,错误次数{errorCount}",f"提示：执行{roundCount}次卡死，完成重启")
                    pass
                else:
                    msh.send_simple_push(f"错误内容:{e}",f"提示：执行{roundCount}次跳出,未知错误")
                    break
                continue

            if roundCount % 10 == 1:
                logging.info(msh.send_simple_push("目标列表数量","提示：卡包运行第{0}轮开始".format(roundCount)))
            # 核心获取逻辑
            try:
                gotFlag = get_card(bagStep, bagTop, bagTagList)
            except Exception as e:
                logging.error(f"错误内容:{e}")
                msh.send_simple_push(f"错误内容:{e}",f"提示：执行{roundCount}次跳出,捕捉错误")
                # 安全设置，当刷取中途报错时切换
                if errorCount == 0:
                    switch_device()
                errorCount += 1
                if errorCount < 10:
                    msh.send_simple_push(f"开始重启,错误次数{errorCount}",f"提示：执行{roundCount}次卡死，开始重启")
                    restart_all()
                    msh.send_simple_push(f"完成重启,错误次数{errorCount}",f"提示：执行{roundCount}次卡死，完成重启")
                    pass
                else:
                    msh.send_simple_push(f"错误内容:{e}",f"提示：执行{roundCount}次跳出,未知错误")
                    break
                continue
            if gotFlag:
                if collectImg:
                    gamer.collect_log_image(f"第{roundCount}次-成功")
                logging.info(msh.send_simple_push(f"卡包", f"提示：获得一个卡包,累计{tagCount}个"))
                gamer.delay(3600)
                save_current_device()
                stayFlag = True
                tagCount += 1
            else:
                # 舍弃现有结果
                if collectImg:
                    gamer.collect_log_image(f"第{roundCount}次-失败")
                gamer.home()
                refreshCount += 1
                stayFlag = False
                # 次设备重置结果
                switch_device()
                # 重置错误次数
                errorCount = 0
            roundCount += 1
        except Exception as e:
            logging.error(f"错误内容:{e}")
            msh.send_simple_push(f"错误内容:{e}",f"提示：执行{roundCount}次跳出,捕捉错误")
            errorCount += 1
            if errorCount < 10:
                msh.send_simple_push(f"开始重启,错误次数{errorCount}",f"提示：执行{roundCount}次卡死，开始重启")
                restart_all()
                msh.send_simple_push(f"完成重启,错误次数{errorCount}",f"提示：执行{roundCount}次卡死，完成重启")
                pass
            else:
                msh.send_simple_push(f"错误内容:{e}",f"提示：执行{roundCount}次跳出,未知错误")
                break
            continue
    logging.info(msh.send_simple_push("源列表为空","提示：完成执行"))
    logging.info("完成执行")

def get_general_items(refreshCount, targetStartNum, targetCount = 25, collectImg = False):
    global stayFlag, switchFlag, currentTarget, targetList, exitFlag, roundFlag
    tagCount = 0
    roundCount = 1
    errorCount = 0
    ADBHelper.connent(deviceID)
    ADBHelper.connent(deviceID2)

    # 初始设置acc
    set_acc_by_item(currentTarget)

    if gho.verify_empty():
        logging.info("测试：目前有空位")
    while True:
        if tagCount >= targetCount:
            break
        if gho.verify_exit():
            exitFlag = True
            break
        try:
            if not stayFlag:
                into_game(True)
            else:
                stayFlag = False

            if len(ADBHelper.getDevicesList()) < 2:
                logging.info(msh.send_simple_push("目标列表为空","提示：重启出现问题，尝试恢复"))
                errorCount += 1
                if errorCount < 3:
                    msh.send_simple_push(f"开始重启,错误次数{errorCount}",f"提示：执行{roundCount}次卡死，开始重启")
                    restart_all()
                    msh.send_simple_push(f"完成重启,错误次数{errorCount}",f"提示：执行{roundCount}次卡死，完成重启")
                    pass
                else:
                    msh.send_simple_push(f"错误内容:{e}",f"提示：执行{roundCount}次跳出,未知错误")
                    break
                continue

            # 检测到1级橘子才收橘子
            if len(ghh.stable_find_board_items(rd.orange_1_stable)) > 0:
                # gho.filter_orange()
                gho.round_all()
                # save_current_device()
                #收橘子可能导致count不正确
                count = len(ghh.stable_find_board_items(currentTarget.get("targetItem"), retryNumMin, targetAcc))
                if currentTarget.get("targetItem2"): 
                    count += len(ghh.stable_find_board_items(currentTarget.get("targetItem2"), retryNumMin, targetAcc))
            
            # 0 初始清理
            if not gho.verify_clean(stepLen):
                if gho.verify_exit():
                    break
                raise Exception(f'清理棋盘失败，未能使空格数量到达: {stepLen}')
            # 1 初始目标物数量
            if roundCount == 1:
                tempList = ghh.stable_find_board_items(currentTarget.get("targetItem"), retryNum, targetAcc)
                logging.info(msh.send_simple_push("在第{0}次执行中，获取列表: {1}".format(roundCount, tempList),f"提示：开始第{roundCount}次执行"))
                count = len(tempList)
                if currentTarget.get("targetItem2"): 
                    count += len(ghh.stable_find_board_items(currentTarget.get("targetItem2"), retryNumMin, targetAcc))
            
            # 2 通用逻辑, 更新目标列表
            point = find_first_resource_point(currentTarget.get("resourceItem"))
            # 当未找到目标时
            if not point: 
                if switchFlag:
                    logging.info(msh.send_simple_push("目标列表为空","提示：目标列表为空"))
                    logging.info("提示：目标列表为空")
                    # if gamer.find_pic_touch(rd.into_board):
                    if not gamer.verify_pic(rd.back_from_board):
                        gamer.home()
                        logging.info(msh.send_simple_push("目标列表为空但未在棋盘内，直接重启","提示：运行第{0}轮异常，尝试重新进入棋盘".format(roundCount)))
                        # 根据经验，这种情况一般已经卡住，直接重启
                        restart_all()
                        gamer.delay(3)
                        continue
                    targetStartNum += 1
                    if targetStartNum < len(targetList):
                        # 更换目标
                        switchFlag = False
                        currentTarget = targetList[targetStartNum]
                        # 更换设置acc
                        set_acc_by_item(currentTarget)
                        logging.info(msh.send_simple_push("目标列表数量","提示：更换目标列表，尝试重新进入棋盘".format(roundCount)))
                        count = len(ghh.stable_find_board_items(currentTarget.get("targetItem"), retryNum, targetAcc))
                        continue
                    else:
                        # 如果没有获取到物品，则进入挂机逻辑
                        if tagCount == 0: 
                            # exitFlag = True
                            roundFlag = False
                        break
                else:
                    switchFlag = True
                    continue
            elif roundCount % 10 == 1:
                logging.info(msh.send_simple_push("目标列表数量","提示：运行第{1}轮开始，总数量{0}".format(count_resource(currentTarget.get("resourceItem")), roundCount)))
            # 当找到目标时
            switchFlag = False

            count = len(ghh.stable_find_board_items(currentTarget.get("targetItem"), retryNumMin, targetAcc))
            if currentTarget.get("targetItem2"): 
                count += len(ghh.stable_find_board_items(currentTarget.get("targetItem2"), retryNumMin, targetAcc))
            logging.info("在第{0}次执行中，目标物起始数量: {1}".format(roundCount, count))
            # 3 操作获取新元素[重要]，操作时若报错，则使用另一个记录
            try:
                # 双击一次
                gamer.clean_touch(point, 2)

                # 获取目前数量
                time.sleep(1)
                # tempList = ghh.find_board_items(currentTarget.get("targetItem"))
                tempList = ghh.stable_find_board_items(currentTarget.get("targetItem"), retryNumMin, targetAcc)
                roundCount += 1
                countNow = len(tempList)
                if currentTarget.get("targetItem2"): 
                    countNow += len(ghh.stable_find_board_items(currentTarget.get("targetItem2"), retryNumMin, targetAcc))
                if roundCount % 5 == 0:
                    logging.info(msh.send_simple_push("在第{0}次执行中，获取列表: {1}".format(roundCount, tempList),f"提示：完成第{roundCount}次执行"))
                logging.info("在第{0}次执行中，目标物列表: {1}".format(roundCount, tempList))
                logging.info("在第{0}次执行中，目标物执行后数量: {1}".format(roundCount, countNow))
            except Exception as e:
                logging.error(f"错误内容:{e}")
                msh.send_simple_push(f"错误内容:{e}",f"提示：执行{roundCount}次跳出,捕捉错误")
                # 安全设置，当刷取中途报错时切换
                if errorCount == 0:
                    switch_device()
                errorCount += 1
                if errorCount < 10:
                    msh.send_simple_push(f"开始重启,错误次数{errorCount}",f"提示：执行{roundCount}次卡死，开始重启")
                    restart_all()
                    msh.send_simple_push(f"完成重启,错误次数{errorCount}",f"提示：执行{roundCount}次卡死，完成重启")
                    pass
                else:
                    msh.send_simple_push(f"错误内容:{e}",f"提示：执行{roundCount}次跳出,未知错误")
                    break
                continue

            # 4 处理产物或刷新
            if countNow > count:
                count = countNow
                # 成功，若需要则合成，并更新count
                if (currentTarget.get("mergeRequired")):
                    simple_merge(currentTarget.get("targetItem"), currentTarget.get("targetAcc"))
                    if currentTarget.get("targetItem2"): 
                        simple_merge(currentTarget.get("targetItem2"), currentTarget.get("targetAcc"))
                if currentTarget.get("consumeItem"):
                    gamer.delay(1)
                    gamer.find_pic_double_touch(currentTarget.get("consumeItem"), resourceAcc)
                gamer.delay(2)
                count = len(ghh.find_board_items(currentTarget.get("targetItem")))
                if currentTarget.get("targetItem2"): 
                    count += len(ghh.stable_find_board_items(currentTarget.get("targetItem2"), retryNumMin, targetAcc))
                # 后续处理
                if collectImg:
                    gamer.collect_log_image(f"第{roundCount}次-成功")
                save_current_device()
                stayFlag = True
                tagCount += 1
                logging.info(msh.send_simple_push(f"源目标物位置：{tempList}", f"提示：获得一个目标物,累计{tagCount}个"))
                logging.info(f"目标物位置：{tempList}")
            else:
                # switch current deviceId to the next
                # 舍弃现有结果
                if collectImg:
                    gamer.collect_log_image(f"第{roundCount}次-失败")
                gamer.home()
                refreshCount += 1
                stayFlag = False
                # 次设备重置结果
                switch_device()
                # 重置错误次数
                errorCount = 0
        # except concurrent.futures.TimeoutError as e:
        except Exception as e:
            logging.error(f"错误内容:{e}")
            msh.send_simple_push(f"错误内容:{e}",f"提示：执行{roundCount}次跳出,捕捉错误")
            errorCount += 1
            if errorCount < 10:
                msh.send_simple_push(f"开始重启,错误次数{errorCount}",f"提示：执行{roundCount}次卡死，开始重启")
                restart_all()
                msh.send_simple_push(f"完成重启,错误次数{errorCount}",f"提示：执行{roundCount}次卡死，完成重启")
                pass
            else:
                msh.send_simple_push(f"错误内容:{e}",f"提示：执行{roundCount}次跳出,未知错误")
                break
            continue
    logging.info(msh.send_simple_push("源列表为空","提示：完成执行"))
    logging.info("完成执行")

def get_power_items(itemPoint, tagList, tagAcc, stepLen, targetWeight, lastWeight = 256, itemImg = rd.fish_source_5, tagListTag = []):
    global stayFlag, switchFlag, currentTarget, targetList, exitFlag, roundFlag
    tagCount = 0
    roundCount = 1
    errorCount = 0
    lastPowerCount = -20
    refreshCount = 0
    i = 0
    ADBHelper.connent(deviceID)
    ADBHelper.connent(deviceID2)

    if gho.verify_empty():
        logging.info("测试：目前有空位")
    while True:
        if gho.verify_exit():
            exitFlag = True
            break
        elif tagNum > 0 and  tagCount > tagNum:
            exitFlag = True
            break
        try:
            if not stayFlag:
                into_game(True)
            else:
                stayFlag = False

            if len(ADBHelper.getDevicesList()) < 2:
                logging.info(msh.send_simple_push("目标列表为空","提示：重启出现问题，尝试恢复"))
                errorCount += 1
                if errorCount < 3:
                    msh.send_simple_push(f"开始重启,错误次数{errorCount}",f"提示：执行{roundCount}次卡死，开始重启")
                    restart_all()
                    msh.send_simple_push(f"完成重启,错误次数{errorCount}",f"提示：执行{roundCount}次卡死，完成重启")
                    pass
                    continue
                else:
                    msh.send_simple_push(f"错误内容:{e}",f"提示：执行{roundCount}次跳出,未知错误")
                    break

            # 检测到1级橘子才收橘子
            if len(ghh.stable_find_board_items(rd.orange_1_stable)) > 0:
                gho.round_all()
                continue

            # 0 初始清理
            # 成功，若需要则合成
            gho.process_existed(tagList[:-1], True, tagAcc)
            if (len(tagListTag) > 0):
                gho.process_existed(tagListTag[:-1], True, tagAcc)

            if not gho.verify_clean(stepLen):
                if gho.verify_exit():
                    break
                raise Exception(f'清理棋盘失败，未能使空格数量到达: {stepLen}')
            if roundCount % 20 == 1:
                gho.clean_up(1)
            # 1 初始目标物数量
            count = ghh.get_total_weight(tagList, tagAcc)
            if (len(tagListTag) > 0):
                count += ghh.get_total_weight(tagListTag, tagAcc) * 4
            logging.info("在第{0}次执行中，初始目标物权重: {1}".format(roundCount, count))
            # 完成后退出
            if count > lastWeight:
                exitFlag = True
                break

            if itemImg:
                itemPoint = find_first_resource_point(itemImg)
                if not itemPoint:
                    break

            # 3 操作获取新元素[重要]，操作时若报错，则使用另一个记录
            try:
                # 双击一次
                gamer.clean_touch(itemPoint, stepLen + 1)
                # 获取目前数量
                time.sleep(1)
                countNow = ghh.get_total_weight(tagList, tagAcc)
                if (len(tagListTag) > 0):
                    countNow += ghh.get_total_weight(tagListTag, tagAcc) * 4
                roundCount += 1
                if roundCount % 5 == 0:
                    logging.info(msh.send_simple_push("在第{0}次执行中，获取列表: {1}".format(roundCount, countNow),f"提示：完成第{roundCount}次执行"))
                logging.info("在第{0}次执行中，现有目标物权重: {1}".format(roundCount, countNow))


                # 3.1 处理体力问题
                # 如果弹出体力提示
                if gho.solve_breaker():
                    # 防止太快使用体力瓶
                    if roundCount - lastPowerCount < (30 // stepLen):
                        logging.info(msh.send_simple_push("在第{0}次执行中，反复卡顿导致退出，当前计数：{1}, 目标物 {2}".format(roundCount, count, tagList),f"错误：第{roundCount}次执行因卡顿退出"))
                        raise Exception(f'使用体力后太快卡顿，尝试重启解决')
                    # 简单处理 本地使用体力瓶，并保存
                    elif settings.usePower and gamer.find_pic_double_touch(rd.power_5, 0.6):
                        # 分支 成功
                        save_current_device()
                        logging.info(msh.send_simple_push("在第{0}次执行中，使用体力，当前计数：{1}, 目标物 {2}, 上次使用体力在{3}".format(roundCount, count, tagList, lastPowerCount),f"提示：第{roundCount}次执行使用体力"))
                        lastPowerCount = roundCount
                        roundCount += 1
                        continue
                    else:
                        # 未知错误
                        gamer.collect_log_image("无可用体力导致退出")
                        logging.info(msh.send_simple_push("在第{0}次执行中，无可用体力导致退出，当前计数：{1}, 目标物 {2}".format(roundCount, count, tagList),f"错误：第{roundCount}次执行因卡顿退出"))
                        if roundFlag:
                            # 体力正常用完时退出
                            break
                        else:
                            # 循环执行时正常等待
                            for i in range(7):
                                gamer.delay(300)
                                if gho.verify_exit():
                                    exitFlag = True
                                    break
                            if i > 5:
                                # 体力正常用完时重试
                                continue
                            else:
                                break
                            

                # 4 处理产物或刷新
                if countNow >= count + targetWeight:
                    count = countNow
                    # 成功，若需要则合成
                    gho.process_existed(tagList[:-1], True, tagAcc)
                    gho.process_existed(tagListTag[:-1], True, tagAcc)
                    # 后续处理
                    save_current_device()
                    stayFlag = True
                    tagCount += 1
                    logging.info(msh.send_simple_push(f"源目标物位置：{tagList[0]}", f"提示：获得一组目标物,累计权重{countNow}"))
                    logging.info(f"目标物权重：{countNow}")
                elif countNow < count + stepLen:
                    logging.info(msh.send_simple_push(f"源目标物位置：{tagList[0]}，更换源目标物", f"提示：获得目标物数量不足,累计权重{countNow}"))
                    save_current_device()
                    continue
                else:
                    # switch current deviceId to the next
                    # 舍弃现有结果
                    gamer.home()
                    refreshCount += 1
                    stayFlag = False
                    # 次设备重置结果
                    switch_device()
                    # 重置错误次数
                    errorCount = 0
            except Exception as e:
                logging.error(f"错误内容:{e}")
                msh.send_simple_push(f"错误内容:{e}",f"提示：执行{roundCount}次跳出,捕捉错误")
                # 安全设置，当刷取中途报错时切换
                if errorCount == 0:
                    switch_device()
                errorCount += 1
                if errorCount < 10:
                    msh.send_simple_push(f"开始重启,错误次数{errorCount}",f"提示：执行{roundCount}次卡死，开始重启")
                    restart_all()
                    msh.send_simple_push(f"完成重启,错误次数{errorCount}",f"提示：执行{roundCount}次卡死，完成重启")
                    pass
                else:
                    msh.send_simple_push(f"错误内容:{e}",f"提示：执行{roundCount}次跳出,未知错误")
                    break
        except Exception as e:
            logging.error(f"错误内容:{e}")
            msh.send_simple_push(f"错误内容:{e}",f"提示：执行{roundCount}次跳出,捕捉错误")
            errorCount += 1
            if errorCount < 10:
                msh.send_simple_push(f"开始重启,错误次数{errorCount}",f"提示：执行{roundCount}次卡死，开始重启")
                restart_all()
                msh.send_simple_push(f"完成重启,错误次数{errorCount}",f"提示：执行{roundCount}次卡死，完成重启")
                pass
                continue
            else:
                msh.send_simple_push(f"错误内容:{e}",f"提示：执行{roundCount}次跳出,未知错误")
                break
    logging.info(msh.send_simple_push("源列表为空","提示：完成执行"))
    logging.info("完成执行")
    # while True:
    #     # if gho.verify_exit():
    #     #     break
    #     time.sleep(1200)
    #     gho.round_all()
    #     logging.info(msh.send_simple_push("结合执行","提示：完成一次结合执行"))

if __name__ == "__main__":
    if startPower > checkPower:
        tagNum = (startPower - checkPower) / 8 - 2
        tagList = tagList[1:]

    if cardFlag:
        get_cards()
    elif roundFlag:
        while not exitFlag:
            get_general_items(refreshCount, targetStartNum, targetCount, collectImg)
            get_power_items(itemPoint, tagList, tagAcc, stepLen, targetWeight, lastWeight, itemImg, tagListTag)
    elif getBoxFlag:
        get_general_items(refreshCount, targetStartNum, 99, collectImg)
    else:
        get_power_items(itemPoint, tagList, tagAcc, stepLen, targetWeight, lastWeight, itemImg, tagListTag)