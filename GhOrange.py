import RaphaelScriptHelper as gamer
import multiprocessing
import testDict as rd
import settings
import pyautogui
import time
import GhHelper as ghh
import pygetwindow as gw
import schedule
import datetime
import ImageProc
import logging
import messageHelper as msh
import GhTemp
from enum import Enum

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
# beikeAcc = 0.65
errorCount = 0
beikeAcc = 0.65
windowID = "BlueStacks App Main"
windowID2 = "BlueStacks App Player 2"
windowID3 = "BlueStacks Multi"
# 首个按钮 150%中 (900, 225), (900, 330), 确认键为 (900, 600)
deviceID = settings.deviceList[0]["deviceId"]
deviceID2 = settings.deviceList[1]["deviceId"]

useCoin = False
useCoin = True
usePower = False
# usePower = True

targetListOrangeTree = settings.targetListOrangeTree

gamer.deviceID = deviceID
targetListBeike = [
    # rd.beike_2,
    rd.beike_3,
    rd.beike_4,
    rd.beike_5_1,
    rd.beike_6,
    rd.beike_7,
    rd.beike_8,
    rd.beike_9,
    rd.beike_10
]

targetListPower = [
    rd.power_1_new,
    rd.power_2_new,
    rd.power_3,
    rd.power_4
]

targetListStone = [
    rd.stone_2,
    rd.stone_3
]

targetListBlue = [
    rd.blue_resource_1,
    rd.blue_resource_2,
    rd.blue_resource_3,
]

targetListFloat = [
    rd.float_2,
    rd.float_3
]

targetListCoin = [
    rd.coin_new_1,
    rd.coin_new_2,
    rd.coin_new_3,
    rd.coin_new_4
]

targetListOrange = [
    rd.orange_1_stable,
    rd.orange_2_stable,
    rd.orange_3_stable,
    rd.orange_4_stable,
    rd.orange_5_stable,
    rd.orange_6_stable
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
        powerCol = gamer.find_pic_all_list(targetListOrange)
        powerCol = ghh.get_collection_unique_grid_positions(powerCol)
        print("在设备{0}中，获取目标个数: {1}".format(gamer.deviceID, powerCol))
        slideCount = ghh.process_collection(powerCol, gamer.slide)
        print("在设备{0}中，获取滑动次数: {1}".format(gamer.deviceID, slideCount))

def process_existed(targetList, cacheFlag = False, accuracy = settings.accuracy):
    slideCount = 1
    totalCount = 0
    if cacheFlag:
        powerCol = gamer.find_pic_all_list_cache(targetList, accuracy)
        powerCol = ghh.get_collection_unique_grid_positions(powerCol)
        print("在设备{0}中，获取目标个数: {1}".format(gamer.deviceID, powerCol))
        slideCount = ghh.process_collection(powerCol, gamer.slide)
        print("在设备{0}中，获取滑动次数: {1}".format(gamer.deviceID, slideCount))
        return slideCount
    else:
        while slideCount > 0:
            # gamer.delay(1)
            powerCol = gamer.find_pic_all_list(targetList, accuracy)
            powerCol = ghh.get_collection_unique_grid_positions(powerCol)
            print("在设备{0}中，获取目标个数: {1}".format(gamer.deviceID, powerCol))
            slideCount = ghh.process_collection(powerCol, gamer.slide)
            totalCount += slideCount
            print("在设备{0}中，获取滑动次数: {1}".format(gamer.deviceID, slideCount))
        return totalCount

def verify_empty():
    time.sleep(1)
    if len(gamer.find_all_empty(ghh.get_all_center())) > 0:
        return True
    else:
        return False

def verify_clean(minNum = 1):
    if not gamer.verify_pic_strict(rd.back_from_board, True):
        gamer.delay(2)
        if not gamer.verify_pic_strict(rd.back_from_board, False):
            gamer.collect_log_image("清理前不正常")
            raise Exception(f'错误：进入棋盘不成功')
    count = len(gamer.find_all_empty(ghh.get_all_center(), True))
    initCount = count
    # 一个格子时，空格数大于0
    minNum = minNum - 1
    if not (count > minNum):
        clean_up(1)
        gamer.delay(0.5)
        count = len(gamer.find_all_empty(ghh.get_all_center()))
        logging.info(msh.send_simple_push(f"检测到棋盘满,剩余空格数{count}",f"提示：一级清理,剩余空格数{count}"))
    if not (count > minNum):
        if useCoin:
            clean_up(2)
            gamer.delay(0.5)
            count = len(gamer.find_all_empty(ghh.get_all_center()))
            logging.info(msh.send_simple_push(f"检测到棋盘满,剩余空格数{count}",f"提示：二级清理,剩余空格数{count}"))
        else:
            logging.info(msh.send_simple_push(f"检测到棋盘满,剩余空格数{count}",f"提示：二级清理,不能使用金币，暂停"))
    if not (count > minNum):
        if useCoin:
            clean_up(3)
            process_existed_orange()
            gamer.delay(0.5)
            count = len(gamer.find_all_empty(ghh.get_all_center()))
            logging.info(msh.send_simple_push(f"检测到棋盘满,剩余空格数{count}",f"提示：三级清理,剩余空格数{count}"))
        else:
            logging.info(msh.send_simple_push(f"检测到棋盘满,剩余空格数{count}",f"提示：三级清理,不能使用金币，暂停"))
    if not (count > minNum):
        if not gamer.verify_pic_strict(rd.back_from_board, True):
            gamer.collect_log_image("清理时不正常")
            raise Exception(f'错误：进入棋盘不成功')
        gamer.collect_log_image("清理棋盘失败")
        if verify_exit():
            raise Exception(f'错误：时间需要退出')
        gamer.delay(600)
        return False
    else:
        # 如果清理过 save
        if count > initCount:
            gamer.home()
            time.sleep(3)
            gamer.find_pic_touch(rd.start_game)
        return True

def verify_exit():
    # return False
    nowTime = datetime.datetime.now().time()
    # if nowTime > datetime.time(4, 14) and nowTime < datetime.time(8, 55): 
    if nowTime > datetime.time(7, 44) and nowTime < datetime.time(8, 55): 
        gamer.collect_log_image()
        time.sleep(3)
        gamer.home()
        time.sleep(3)
        gamer.collect_log_image()
        return True
    else:
        return False

# def verify_exit():
#     return False

# temp = ImageProc.get_color(rd.empty_blue_2,(64,64))
# print("在设备{0}中，获取目标个数: {1}".format(gamer.deviceID, powerCol[0]))
# temp = gamer.find_all_empty(ghh.get_all_center())
# print("temp:{0}".format(temp))

# 点击贝壳发射器
# gamer.touch(ghh.get_center((1,5)))


# 此处为收橘子完整逻辑
def filter_orange():
    count = 0
    tryCount = 0
    for tree in targetListOrangeTree:
        tryCount = 0
        while tryCount < 30:
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
            # 测试，防止被打断
            solve_breaker()
            process_existed_orange()
            verify_clean()
            tryCount += 1
            # if useCoin:
            #     if not verify_empty():
            #         logging.info(msh.send_simple_push("进入页面时","提示：棋盘已满，进入前完全清理"))
            #         clean_up(3)
                    # ghh.click_order(rd.order_orange)
            
            # 暂时 安全措施，防止无限卡死
            # if datetime.datetime.now().time() > datetime.time(7, 55): 
            #     gamer.collect_log_image('orange_err')
            #     time.sleep(3)
            #     gamer.home()
            #     time.sleep(3)
            #     gamer.collect_log_image('orange_err')
            #     break
        if tryCount > 29:
            gamer.collect_log_image()
        count += 1
        if count%8 == 0:
            clean_up(1)
    process_existed_orange()
def filter_beike(count = 6):
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
        morning_clean()
        process_existed(targetListCoin, True)
        #temp
        process_existed(targetListPower, True)
        process_existed_orange()
        # process_existed(targetListStone)
        # gamer.find_pic_double_touch(rd.stone_4)

        # process_existed(targetListBlue)
        gamer.delay(1)
    elif type == 2: 
        clean_up(1)
        # process_existed(targetListFloat)
        gamer.delay(1)
        gamer.find_pic_double_touch(rd.coin_new_5)
        gamer.find_pic_double_touch(rd.coin_new_4)
        # gamer.find_pic_double_touch(rd.float_4)
    else:
        clean_up(2)
        # gamer.find_pic_double_touch(rd.icon_4)
        # process_existed(targetListBeike)
        gamer.find_pic_double_touch(rd.coin_new_3)
        gamer.find_pic_double_touch(rd.coin_new_2)
        gamer.find_pic_double_touch(rd.coin_new_1)
        # gamer.find_pic_double_touch(rd.float_3)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')



# 简单功能测试

def round_all():
    if useCoin:
        # if verify_empty():
        #     clean_up(2)
        # else:
        gamer.home()
        time.sleep(3)
        GhTemp.into_game(True)
        if not verify_empty():
            logging.info(msh.send_simple_push("进入页面时","提示：棋盘已满，进入前完全清理"))
            clean_up(3)
            # ghh.click_order(rd.order_orange)
    filter_orange()
    if useCoin and usePower:
        for i in range(1,30):
            filter_beike()
            # if gamer.verify_pic(rd.back_from_board):
            if solve_breaker():
                process_existed(targetListBeike)
                break
            process_existed(targetListBeike)
            if verify_empty():
                clean_up(2)
            else:
                logging.info(msh.send_simple_push("1","提示：棋盘已满，完成后完全清理"))
                clean_up(3)
                # ghh.click_order(rd.order_orange)
    gamer.home()
    gamer.delay(5)  # 等待窗口激活
    gamer.find_pic_touch(rd.start_game)
    logging.info(msh.send_simple_push("1","提示：完成一轮执行"))
    logging.info("完成执行")

def morning_clean():
    if gamer.verify_pic(rd.daily_info):
        gamer.touch(rd.daily_close)

def draft():
    if(gamer.verify_pic(rd.out_of_power_1)):
        gamer.touch(rd.close_button)
        gamer.delay(3)
        if(gamer.verify_pic(rd.out_of_power_1)):
            logging.error("未能正确离开无体力状态")
            msh.send_simple_push("1","错误：未能离开无体力状态")
            # continue
        logging.info("正确离开无体力状态")
        # msh.send_simple_push("1","提示：正确离开无体力状态")
        process_existed(targetListBeike)
        clean_up(2)
        # break
    if(gamer.verify_pic(rd.out_of_power_2)):
        gamer.touch(rd.out_of_power_2_button)
        gamer.delay(3)
        if(gamer.verify_pic(rd.out_of_power_2)):
            logging.error("未能正确离开无体力状态")
            msh.send_simple_push("1","错误：未能离开无体力状态")
            # continue
        logging.info("正确离开无体力状态")
        # msh.send_simple_push("1","提示：正确离开无体力状态")
        process_existed(targetListBeike, False, beikeAcc)
        clean_up(2)
        # break

def leave_incident_with_normal_flag():
    if gamer.verify_pic_strict(rd.back_from_board):
        return True
    elif gamer.find_pic_touch(rd.into_board):
        gamer.delay(6)
        return False
    else:
        gamer.back()
        gamer.delay(3)
        return False
def solve_breaker():
    count = 0
    while not leave_incident_with_normal_flag():
        count += 1
        if count == 10:
            # 尝试解决1
            # gamer.touch((931, 1864))
            msh.send_simple_push("解决次数大于10","提示：尝试点击解决阻塞问题")
        if count > 20:
            msh.send_simple_push("错误出现20次","错误：未能离开无体力状态")
            raise Exception(f'错误：未能解决卡顿')
    if count > 0:
        msh.send_simple_push("解决次数大于0","提示：解决一次阻塞问题")
        return True
    else: return False
    
# 测试
if __name__ == "__main__":
    # settings.accuracy = 0.75
    # 对多贝壳订单临时改进
    # settings.accuracy = 0.70
    # process_existed(targetListBeike)
    # round_all()
    # 设置定时任务
    # schedule.every().hour.at(":05").do(round_all)  # 每小时 0 分钟
    schedule.every().hour.at(":10").do(round_all)  # 每小时 20 分钟
    schedule.every().hour.at(":40").do(round_all)  # 每小时 40 分钟

    print("定时任务已启动，等待运行...")

    # 保持程序运行
    while True:
        try:
            schedule.run_pending()  # 运行待执行的任务
            if datetime.datetime.now().time() > datetime.time(7, 55): 
                gamer.collect_log_image('orange_fin_1')
                time.sleep(3)
                gamer.home()
                time.sleep(3)
                gamer.collect_log_image('orange_fin_2')
                break
            time.sleep(5)  # 每5秒检查一次
            nowTime = datetime.datetime.now().time()
            if nowTime > datetime.time(4, 9) and nowTime < datetime.time(4, 20):
                usePower = True
            elif nowTime > datetime.time(7, 39) and nowTime < datetime.time(7, 50):
                usePower = True
            else: usePower = False
        except Exception as e:
            errorCount += 1
            if errorCount < 3:
                msh.send_simple_push(f"开始重启,错误次数{errorCount}",f"提示：卡死，开始重启")
                GhTemp.restart_all()
                msh.send_simple_push(f"完成重启,错误次数{errorCount}",f"提示：卡死，完成重启")
                pass
            else:
                msh.send_simple_push(f"错误内容:{e}",f"提示：跳出,未知错误")
                raise