import RaphaelScriptHelper as gamer
import multiprocessing
import testDict as rd
import settings
import pyautogui
import time
import GhHelper as ghh
import GhEventHelper as gheh
import ImageProc
import logging
import messageHelper as msh
import GhOrange as gho
import ADBHelper
import concurrent.futures
import datetime
from enum import Enum

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class IntoGameEnum(Enum):
    START = settings.eventIntoGameList[0]
    CLOUD = settings.eventIntoGameList[1]
    INTO = settings.eventIntoGameList[2]
    AT = settings.eventIntoGameList[3]

intoGameList = settings.eventIntoGameList
deviceID = settings.deviceList[0]["deviceId"]
deviceID2 = settings.deviceList[1]["deviceId"]
resourcePoint = settings.event_first_block

gamer.deviceID = deviceID
errorCount = 0
roundCount = 1
refreshCount = 1
tagCount = 0
settings.accuracy = 0.75
stayFlag = False
retryNum = 1
retryNumMin = 1
minAccuracy = 0.40
# startAtOrange = False
# startAtOrange = True

# resourceItem = rd.daily_box_3
# targetItem = rd.power_3
# mergeRequired = True
# 重要
gho.useCoin = False
gho.usePower = False
# gho.useCoin = True
# gho.usePower = True
# startAtOrange = 0
refreshCount = 1
# card_1 = 2
# daily_box_3 = 4
targetStartNum = 0
totalCount = 110

targetList = [
    {"targetItem": settings.eventTagList[0], "targetAcc":0.75, "mergeRequired": True},
]
currentTarget = targetList[targetStartNum]

targetListCoin = [
    rd.coin_0,
    rd.coin_new_1,
    rd.coin_new_2,
    rd.coin_new_3,
    rd.coin_new_4
]

targetListPower = [
    rd.power_1_new,
    rd.power_2_new,
    rd.power_3,
    rd.power_4
]

targetListItem = settings.eventItemList

targetListTag = settings.eventTagList

def process_existed(targetList, acc, cacheFlag = False):
    slideCount = 1
    if cacheFlag:
        powerCol = gamer.find_pic_all_list_cache(targetList, acc)
        powerCol = gheh.get_collection_unique_grid_positions(powerCol)
        print("在设备{0}中，获取目标个数: {1}".format(gamer.deviceID, powerCol))
        slideCount = gheh.process_collection(powerCol, gamer.slide)
        print("在设备{0}中，获取滑动次数: {1}".format(gamer.deviceID, slideCount))
    else:
        while slideCount > 0:
            # gamer.delay(1)
            powerCol = gamer.find_pic_all_list(targetList, acc)
            powerCol = gheh.get_collection_unique_grid_positions(powerCol)
            print("在设备{0}中，获取目标个数: {1}".format(gamer.deviceID, powerCol))
            slideCount = gheh.process_collection(powerCol, gamer.slide)
            print("在设备{0}中，获取滑动次数: {1}".format(gamer.deviceID, slideCount))

def clean_event():
    gamer.screenCap()
    process_existed(targetListItem, 0.75, True)
    gamer.screenCap()
    process_existed(targetListTag, 0.75, True)
    process_existed(targetListCoin, 0.50, True)
    # process_existed(targetListPower, 0.775, True)
    process_existed(targetListPower, 0.775, True)
    # gamer.find_pic_double_touch(rd.coin_new_5)

def into_game(verifyIntoFlag = False):
    global intoGameList
    continueFlag = True
    doneIntoFlag = False
    retryCount = 0
    gamer.home()
    gamer.delay(3)
    while continueFlag:
        totalList = gamer.find_pic_all_list(intoGameList)
        totalDict = gheh.combine_lists_to_dict(intoGameList, totalList)
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
                    case IntoGameEnum.INTO.value: 
                        gamer.touch(totalDict[key][0])
                        # 如果不需要确认已进入，则直接跳出，否则依赖back_from_board跳出
                        # if not verifyIntoFlag:
                        #     continueFlag = False
                        # else:
                        #     #防止截图过快导致的后续问题
                        #     doneIntoFlag = True
                        #     time.sleep(2)
                        # break
                        time.sleep(2)
                    # back_from_board
                    case IntoGameEnum.AT.value: 
                        time.sleep(5)
                        if not gamer.verify_pic(IntoGameEnum.AT.value):
                            logging.info("重试进入活动")
                            msh.send_simple_push(f"错误内容",f"提示：跳出,重试进入活动")
                            break
                        else:
                            continueFlag = False
                            break
                        # if doneIntoFlag:
                        #     logging.info(f"已点击进入棋盘，跳过额外验证")
                        #     continueFlag = False
                        #     break
                        # if verifyIntoFlag:
                        #     time.sleep(3)
                        # else:
                        #     time.sleep(7)
                        # # 始终未刷新，可能已经自动保存，则不做处理
                        # if(gamer.verify_pic(rd.back_from_board)):
                        #     logging.info(f"正常刷新，5秒后依旧在棋盘内")
                        #     continueFlag = False
                        #     break
                        # else:
                        #     time.sleep(5)
                        #     if(gamer.verify_pic(rd.back_from_board)):
                        #         logging.info(f"异常刷新，但10秒后依旧在棋盘内，已解决")
                        #         continueFlag = False
                        #         break
                        #     # 重新尝试整个刷新逻辑
                        #     break
                    # 其他操作，需要等待结果
                    case _:
                        retryCount = 0
                        gamer.touch(totalDict[key][0])
                        time.sleep(5)
                        break
        # 一轮识别后的处理
        retryCount += 1
        if retryCount % 30 == 0 and continueFlag:
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
    gamer.delay(25)
    gamer.run_bluestacks_instance(settings.deviceList[0]["instance_title"])
    gamer.run_bluestacks_instance(settings.deviceList[1]["instance_title"])
    gamer.delay(35)
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

def save_main_device():
    gamer.deviceID = deviceID
    gamer.home()
    time.sleep(3)  # 等待窗口激活
    gamer.find_pic_touch(rd.start_game)
    time.sleep(5)  # 等待窗口激活

def save_current_device():
    gamer.home()
    time.sleep(3)  # 等待窗口激活
    gamer.find_pic_touch(rd.start_game)
    time.sleep(5)  # 等待窗口激活

def resume_main_device(waitSeconds = 3):
    # 新的启动流程流程
    gamer.deviceID = deviceID
    gamer.home()
    time.sleep(1)  # 等待窗口激活
    into_game(True)
    time.sleep(waitSeconds)  # 等待窗口激活

def count_resource(target):
    return len(gheh.stable_find_board_items(target, retryNum, minAccuracy))

def find_first_resource_point(target, remainNum = 0):
    resourceList = gheh.stable_find_board_items(target, retryNum, minAccuracy)
    logging.info("find_first_resource_point for {0} get number {1}, when remainNum {2}".format(target, len(resourceList), remainNum))
    if len(resourceList) > remainNum:
        return resourceList[0]
    else:
        return False

def simple_merge(target):
    current_list = gheh.stable_find_board_items(target, retryNum)
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

def quick_merge(current_list):
    # 跳过无效列表记录
    if len(current_list) < 3:
        status = "empty" if not current_list else "just 2-element"
        logging.info(f"simple_merge ({status}) skipped")

    merged_results = []
    # 持续处理直到剩余元素不足两个
    while len(current_list) >= 3:
        # 总是取出前两个元素
        a = current_list.pop(0)
        b = current_list.pop(0)
        merged_results.append(gamer.slide(a, b))
        # 实时日志
        logging.debug(f"Merged ({a}, {b}) for target {current_list}")

def reset_game_with_error_restart():
    """循环中的逻辑"""
    max_retries = 3  # 最大重试次数
    retry_count = 0  # 当前重试次数

    while retry_count < max_retries:
        try:
            # 尝试调用两个方法
            reset_sub_device()
            resume_main_device()
            print("重启覆盖记录成功")
            return  # 如果成功，退出循环
        except Exception as e:
            # logging.error(f"错误内容:{e}")
            # msh.send_simple_push(f"错误内容:{e}",f"提示：执行{roundCount}次跳出,捕捉错误")
            gamer.collect_log_image()
            print(f"发生异常: {e}")
            retry_count += 1
            if retry_count < max_retries:
                print(f"重试次数: {retry_count}")
                msh.send_simple_push(f"重试次数: {retry_count}","提示：进入游戏卡死，开始重启")
                restart_all() # 调用恢复方法
                msh.send_simple_push(f"重试次数: {retry_count}","提示：进入游戏卡死，完成重启")
            else:
                msh.send_simple_push("完成重启","错误：重试次数已达上限，退出程序")
                print("重试次数已达上限，退出程序")
                raise  # 抛出异常并退出程序

# [脚本从这里开始运行]
ADBHelper.connent(deviceID2)

if __name__ == "__main__":
    ADBHelper.connent(deviceID)
    ADBHelper.connent(deviceID2)
    while True:
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
                break

            count = len(gheh.stable_find_board_items(currentTarget["targetItem"], retryNumMin))

            # 1 初始目标物数量
            if roundCount == 1:
                tempList = gheh.stable_find_board_items(currentTarget["targetItem"], retryNum)
                logging.info(msh.send_simple_push("在第{0}次执行中，获取列表: {1}".format(roundCount, tempList),f"提示：开始第{roundCount}次执行"))
                count = len(tempList)
            
            # 2 通用逻辑, 更新目标列表[直接为固定值]
            # resourcePoint = settings.event_first_block

            # 3 操作获取新元素[重要]，操作时若报错，则使用另一个记录
            try:
                # 双击一次
                # gamer.clean_touch(resourcePoint, 2)
                gamer.touch(resourcePoint)
                #暂时 多次点击
                # gamer.delay(1)
                # gamer.touch(resourcePoint)
                # gamer.delay(1)
                # gamer.touch(resourcePoint)

                if tagCount > 70:
                    logging.info(f"轮数{tagCount}较多，提前清理")
                    clean_event()

                # 获取目前数量
                time.sleep(3)
                # tempList = gheh.find_board_items(currentTarget["targetItem"])
                tempList = gheh.stable_find_board_items(currentTarget["targetItem"], retryNumMin, 0.65)
                roundCount += 1
                countNow = len(tempList)
                if roundCount % 5 == 0:
                    logging.info(msh.send_simple_push("在第{0}次执行中，获取列表: {1}".format(roundCount, tempList),f"提示：完成第{roundCount}次执行"))
                logging.info("在第{0}次执行中，目标物列表: {1}".format(roundCount, tempList))
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

            # 4 处理产物或刷新
            if countNow > count:
            # if countNow >= count:
            # 暂时，更新单个物品
            # if True:
                logging.info(f"countNow:{countNow}, count:{count}")
                count = countNow
                # 成功，若需要则合成，并更新count
                if (currentTarget["mergeRequired"]):
                    # simple_merge(currentTarget["targetItem"])
                    quick_merge(tempList)
                    # gho.clean_up(1)
                    clean_event()
                gamer.delay(2)
                count = len(gheh.stable_find_board_items(currentTarget["targetItem"], retryNumMin, 0.65))
                # 暂时，允许中途退出
                if tagCount > totalCount-1:
                    break
                # 后续处理
                # 暂时取消
                save_current_device()
                stayFlag = True
                tagCount += 1

                logging.info(msh.send_simple_push(f"源目标物位置：{tempList}", f"提示：获得一个目标物,累计{tagCount}个"))
                logging.info(f"目标物位置：{tempList}")
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
            if tagCount > totalCount-1:
                break
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
    logging.info(msh.send_simple_push("源列表为空","提示：完成执行"))
    logging.info("完成执行")
    # while True:
    #     time.sleep(1200)
    #     # gho.round_all()
    #     logging.info(msh.send_simple_push("结合执行","提示：完成一次结合执行"))