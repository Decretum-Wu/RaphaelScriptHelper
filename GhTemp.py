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

intoGameList = [
    rd.start_game,
    rd.cloud_button,
    rd.into_board,
    rd.back_from_board
    ]
windowID3 = "BlueStacks Multi"
deviceID = "emulator-5554"
deviceID2 = "127.0.0.1:5635"
# deviceID = "emulator-5584"
# deviceID = "127.0.0.1:5585"
# deviceID2 = "127.0.0.1:5615"
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
retryNum = 9
retryNumMin = 3
minAccuracy = 0.55
targetMinAccuracy = 0.55
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
targetStartNum = 1
# targetList = [
#     {"resourceItem": rd.license_box_1, "targetItem": rd.stone_3, "mergeRequired": True},
#     {"resourceItem": rd.license_box_2_1, "targetItem": rd.stone_3, "mergeRequired": True},
#     {"resourceItem": rd.license_box_3, "targetItem": rd.blue_resource_1, "mergeRequired": True},
    # {"resourceItem": rd.card_1, "targetItem": rd.stone_4, "mergeRequired": False, "consumeItem": rd.stone_4},
#     {"resourceItem": rd.box_1, "targetItem": rd.power_4, "mergeRequired": True},
#     {"resourceItem": rd.daily_box_3, "targetItem": rd.power_3, "mergeRequired": True},
#     {"resourceItem": rd.daily_box_3, "targetItem": rd.power_3, "mergeRequired": True},
# ]

# targetList = [
#     {"resourceItem": rd.card_1, "targetItem": rd.stone_4, "mergeRequired": False},
#     {"resourceItem": rd.jingxi_box_3, "targetItem": rd.stone_3, "mergeRequired": True},
#     {"resourceItem": rd.rubin_box, "targetItem": rd.stone_2, "mergeRequired": True},
#     {"resourceItem": rd.box_1, "targetItem": rd.power_4, "mergeRequired": True},
#     {"resourceItem": rd.daily_box_3, "targetItem": rd.power_3, "mergeRequired": True},
# ]

targetList = [
    # {"resourceItem": rd.license_box_1, "targetItem": rd.stone_3, "mergeRequired": True},
    # {"resourceItem": rd.license_box_2_1, "targetItem": rd.stone_3, "mergeRequired": True},
    # {"resourceItem": rd.license_box_3, "targetItem": rd.blue_resource_1, "mergeRequired": True},
    # {"resourceItem": rd.licence_box_3_max, "targetItem": rd.stone_4, "mergeRequired": False, "consumeItem": rd.stone_4},
    {"resourceItem": rd.card_1, "targetItem": rd.stone_4, "mergeRequired": False, "consumeItem": rd.stone_4},
    {"resourceItem": rd.coin_box, "targetItem": rd.coin_new_4, "mergeRequired": True, "consumeItem": rd.coin_new_5},
    {"resourceItem": rd.box_1, "targetItem": rd.power_4, "mergeRequired": True},
    {"resourceItem": rd.box_1, "targetItem": rd.power_4, "mergeRequired": True},
    {"resourceItem": rd.box_1, "targetItem": rd.power_4, "mergeRequired": True},
    # {"resourceItem": rd.daily_box_3, "targetItem": rd.power_3, "mergeRequired": True},
]

# targetList = [
#     # {"resourceItem": rd.license_box_1, "targetItem": rd.stone_3, "mergeRequired": True},
#     # {"resourceItem": rd.license_box_2_1, "targetItem": rd.stone_3, "mergeRequired": True},
#     # {"resourceItem": rd.license_box_3, "targetItem": rd.blue_resource_1, "mergeRequired": True},
#     # {"resourceItem": rd.card_1, "targetItem": rd.stone_4, "mergeRequired": False, "consumeItem": rd.stone_4},
#     # {"resourceItem": rd.licence_box_3_max, "targetItem": rd.stone_4, "mergeRequired": False, "consumeItem": rd.stone_4},
#     # {"resourceItem": rd.coin_box, "targetItem": rd.coin_new_4, "mergeRequired": True, "consumeItem": rd.coin_new_5},
#     {"resourceItem": rd.box_1, "targetItem": rd.power_4, "mergeRequired": True},
#     {"resourceItem": rd.box_1, "targetItem": rd.power_4, "mergeRequired": True},
#     # {"resourceItem": rd.daily_box_3, "targetItem": rd.power_3, "mergeRequired": True},
#     # {"resourceItem": rd.daily_box_3, "targetItem": rd.power_3, "mergeRequired": True},
#     # {"resourceItem": rd.daily_box_3, "targetItem": rd.power_3, "mergeRequired": True},
#     # {"resourceItem": rd.daily_box_3, "targetItem": rd.power_3, "mergeRequired": True},
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
                            time.sleep(10)
                        else:
                            time.sleep(10)
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
        if retryCount % 40 == 0 and continueFlag:
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
    gamer.delay(10)
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
    return len(ghh.stable_find_board_items(target, retryNum, minAccuracy))

def find_first_resource_point(target, remainNum = 0):
    resourceList = ghh.stable_find_board_items(target, retryNum, minAccuracy)
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

def get_general_items(refreshCount, targetStartNum):
    global stayFlag, currentTarget, targetList
    tagCount = 0
    roundCount = 1
    errorCount = 0
    ADBHelper.connent(deviceID)
    ADBHelper.connent(deviceID2)
    if gho.verify_empty():
        logging.info("测试：目前有空位")
    while True:
        if gho.verify_exit():
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
                break

            # if refreshCount % 15 == 0:
            # 检测到1级橘子才收橘子
            if len(ghh.stable_find_board_items(rd.orange_1_stable)) > 0:
                # gho.filter_orange()
                gho.round_all()
                # save_current_device()
                #收橘子可能导致count不正确
                count = len(ghh.stable_find_board_items(currentTarget.get("targetItem"), retryNumMin, targetMinAccuracy))
            
            # 0 初始清理
            gho.verify_clean()
            # 1 初始目标物数量
            if roundCount == 1:
                tempList = ghh.stable_find_board_items(currentTarget.get("targetItem"), retryNum, targetMinAccuracy)
                logging.info(msh.send_simple_push("在第{0}次执行中，获取列表: {1}".format(roundCount, tempList),f"提示：开始第{roundCount}次执行"))
                count = len(tempList)
            
            # 2 通用逻辑, 更新目标列表
            point = find_first_resource_point(currentTarget.get("resourceItem"))
            if not point: 
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
                    currentTarget = targetList[targetStartNum]
                    logging.info(msh.send_simple_push("目标列表数量","提示：更换目标列表，尝试重新进入棋盘".format(roundCount)))
                    count = len(ghh.stable_find_board_items(currentTarget.get("targetItem"), retryNum, targetMinAccuracy))
                    continue
                else:
                    break
            elif roundCount % 10 == 1:
                logging.info(msh.send_simple_push("目标列表数量","提示：运行第{1}轮开始，总数量{0}".format(count_resource(currentTarget.get("resourceItem")), roundCount)))

            count = len(ghh.stable_find_board_items(currentTarget.get("targetItem"), retryNumMin, targetMinAccuracy))
            # 3 操作获取新元素[重要]，操作时若报错，则使用另一个记录
            try:
                # 双击一次
                gamer.clean_touch(point, 2)

                # 获取目前数量
                time.sleep(1)
                # tempList = ghh.find_board_items(currentTarget.get("targetItem"))
                tempList = ghh.stable_find_board_items(currentTarget.get("targetItem"), retryNumMin, targetMinAccuracy)
                roundCount += 1
                countNow = len(tempList)
                if roundCount % 5 == 0:
                    logging.info(msh.send_simple_push("在第{0}次执行中，获取列表: {1}".format(roundCount, tempList),f"提示：完成第{roundCount}次执行"))
                logging.info("在第{0}次执行中，目标物列表: {1}".format(roundCount, tempList))
            except Exception as e:
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
                count = countNow
                # 成功，若需要则合成，并更新count
                if (currentTarget.get("mergeRequired")):
                    simple_merge(currentTarget.get("targetItem"))
                if currentTarget.get("consumeItem"):
                    gamer.find_pic_double_touch(currentTarget.get("consumeItem"), minAccuracy)
                gamer.delay(2)
                count = len(ghh.find_board_items(currentTarget.get("targetItem")))
                # 后续处理
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
    while True:
        if gho.verify_exit():
            break
        time.sleep(1200)
        gho.round_all()
        logging.info(msh.send_simple_push("结合执行","提示：完成一次结合执行"))
# [脚本从这里开始运行]

if __name__ == "__main__":
    get_general_items(refreshCount, targetStartNum)