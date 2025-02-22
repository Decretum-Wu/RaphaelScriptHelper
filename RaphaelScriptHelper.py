import ImageProc, ADBHelper, random, time, cv2
import settings as st
import pygetwindow as gw
import pyautogui
import shutil
from datetime import datetime
import concurrent.futures
import time
import subprocess

deviceType = 1
timeout = 8
deviceID = ""
pyautogui.FAILSAFE = False
# windowID = ""

def random_delay():
    t = random.uniform(st.randomDelayMin, st.randomDelayMax)
    print("【随机延时】将随机延时 {0} 秒".format(t))
    time.sleep(t)

def delay(t):
    print("【主动延时】延时 {0} 秒".format(t))
    time.sleep(t)

def random_pos(pos):
    x, y = pos
    rand = random.randint(1, 10000)
    # TODO debug, 增加3点击偏移
    # x = x + 3
    if rand % 2 == 0:
        x = x + random.randint(0, st.touchPosRange)
    else:
        x = x - random.randint(0, st.touchPosRange)

    rand = random.randint(1, 10000)
    if rand % 2 == 0:
        y = y + random.randint(0, st.touchPosRange)
    else:
        y = y - random.randint(0, st.touchPosRange)

    return (x, y)

# 智能模拟点击某个点，将会随机点击以这个点为中心一定范围内的某个点，并随机按下时长
def touch(pos):
    randTime = random.randint(0, st.touchDelayRange)
    _pos = random_pos(pos)
    print("【模拟点击】点击坐标 {0} {1} 毫秒".format(_pos, randTime))
    if randTime < 10:
        ADBHelper.touch(deviceID, _pos)
    else:
        ADBHelper.longTouch(deviceID, _pos, randTime)

# 智能模拟滑屏，给定起始点和终点的二元组，模拟一次随机智能滑屏
# def slide(vector):
#     startPos, stopPos = vector
#     _startPos = random_pos(startPos)
#     _stopPos = random_pos(stopPos)
#     randTime = random.randint(st.slideMinVer, st.slideMaxVer)
#     print("【模拟滑屏】使用 {0} 毫秒从坐标 {1} 滑动到坐标 {2}".format(randTime, _startPos, _stopPos))
#     ADBHelper.slide(deviceID, _startPos, _stopPos, randTime)
#     return stopPos

def slide(startPos, stopPos):
    _startPos = random_pos(startPos)
    _stopPos = random_pos(stopPos)
    randTime = random.randint(st.slideMinVer, st.slideMaxVer)
    print("【模拟滑屏】使用 {0} 毫秒从坐标 {1} 滑动到坐标 {2}".format(randTime, _startPos, _stopPos))
    ADBHelper.slide(deviceID, _startPos, _stopPos, randTime)
    return stopPos

# 截屏，识图，返回坐标
def find_pic(target, returnCenter = False):
    ADBHelper.screenCapture(deviceID, st.cache_path + "screenCap.png")
    time.sleep(0.1)
    if returnCenter == True:
        leftTopPos = ImageProc.locate(st.cache_path + "screenCap.png", target, st.accuracy)
        img = cv2.imread(target)
        centerPos = ImageProc.centerOfTouchArea(img.shape, leftTopPos)
        return centerPos
    else:
        leftTopPos = ImageProc.locate(st.cache_path + "screenCap.png", target, st.accuracy)
        return leftTopPos

# 截屏，识图，返回所有坐标
def find_pic_all(target):
    ADBHelper.screenCapture(deviceID, st.cache_path + "screenCap.png")
    time.sleep(0.1)
    # locate_all
    leftTopPos = ImageProc.locate_all_center(st.cache_path + "screenCap.png", target, st.accuracy)
    return sorted(leftTopPos)

def find_pic_all_stable(target):
    time.sleep(1.5)
    resourceList = find_pic_all(target)
    if len(resourceList) == 0:
        time.sleep(2)
        resourceList = find_pic_all(target)
    if len(resourceList) == 0:
        time.sleep(3)
        resourceList = find_pic_all(target)
    return resourceList

# 截屏，识图，返回所有坐标
def debug_find_pic_all(target):
    # locate_all
    leftTopPos = ImageProc.locate_all_center(st.cache_path + "screenCapTest.png", target, 0.7)
    return leftTopPos

# 截屏，识图，返回所有坐标
def find_pic_all_list(*args):
    ADBHelper.screenCapture(deviceID, st.cache_path + "screenCap.png")
    time.sleep(0.1)
    # locate_all
    if len(args) == 1:
        leftTopPos = ImageProc.locate_all_center_list(st.cache_path + "screenCap.png", args[0], st.accuracy)
    elif len(args) == 2:
        leftTopPos = ImageProc.locate_all_center_list(st.cache_path + "screenCap.png", args[0], args[1])
    else:
        print(f"Multiple arguments: {args}")
        leftTopPos = ImageProc.locate_all_center_list(st.cache_path + "screenCap.png", args[0], st.accuracy)
    return leftTopPos

# 截屏，识图，返回所有坐标
def find_pic_all_list_cache(*args):
    # ADBHelper.screenCapture(deviceID, st.cache_path + "screenCap.png")
    # time.sleep(0.1)
    # locate_all
    if len(args) == 1:
        leftTopPos = ImageProc.locate_all_center_list(st.cache_path + "screenCap.png", args[0], st.accuracy)
    elif len(args) == 2:
        leftTopPos = ImageProc.locate_all_center_list(st.cache_path + "screenCap.png", args[0], args[1])
    else:
        print(f"Multiple arguments: {args}")
    leftTopPos = ImageProc.locate_all_center_list(st.cache_path + "screenCap.png", args[0], st.accuracy)
    return leftTopPos

def find_all_empty(pointList):
    ADBHelper.screenCapture(deviceID, st.cache_path + "screenCap.png")
    time.sleep(0.1)
    resultPointList = ImageProc.find_matching_coordinates(st.cache_path + "screenCap.png", pointList, st.empty_colors)
    return resultPointList

# 判断图片是否存在
def verify_pic(target):
    ADBHelper.screenCapture(deviceID, st.cache_path + "screenCap.png")
    time.sleep(0.1)
    leftTopPos = ImageProc.locate(st.cache_path + "screenCap.png", target, st.accuracy)
    if (leftTopPos): return True
    else: return False

def verify_pic_strict(target):
    ADBHelper.screenCapture(deviceID, st.cache_path + "screenCap.png")
    time.sleep(0.1)
    leftTopPos = ImageProc.locate(st.cache_path + "screenCap.png", target, 0.9999)
    if (leftTopPos): return True
    else: return False

# 寻找目标区块并在其范围内随机点击
def find_pic_touch(target):
    leftTopPos = find_pic(target)
    if leftTopPos is None:
        print("【识图】识别 {0} 失败".format(target))
        return False
    print("【识图】识别 {0} 成功，图块左上角坐标 {1}".format(target, leftTopPos))
    img = cv2.imread(target)
    tlx, tly = leftTopPos
    h_src, w_src, tongdao = img.shape
    # 模拟点击 debug, 3水平偏移
    x = random.randint(tlx + 3, tlx + w_src)
    y = random.randint(tly, tly + h_src)
    touch((x, y))
    return True

def find_pic_double_touch(target):
    leftTopPos = find_pic(target)
    if leftTopPos is None:
        print("【识图】识别 {0} 失败".format(target))
        return False
    print("【识图】识别 {0} 成功，图块左上角坐标 {1}".format(target, leftTopPos))
    img = cv2.imread(target)
    tlx, tly = leftTopPos
    h_src, w_src, tongdao = img.shape
    # 模拟点击 debug, 3水平偏移
    x = random.randint(tlx + 3, tlx + w_src)
    y = random.randint(tly, tly + h_src)
    touch((x, y))
    delay(0.1)
    touch((x, y))
    return True

# 寻找目标区块并将其拖动到某个位置
def find_pic_slide(target,pos):
    leftTopPos = find_pic(target)
    if leftTopPos is None:
        print("【识图】识别 {0} 失败".format(target))
        return False
    print("【识图】识别 {0} 成功，图块左上角坐标 {1}".format(target, leftTopPos))
    img = cv2.imread(target)
    centerPos = ImageProc.centerOfTouchArea(img.shape,leftTopPos)
    slide((centerPos, pos))
    return True

def init_window_save(windowID):
    # 查找并激活目标窗口
    windows = gw.getWindowsWithTitle(windowID)
    if windows:
        window = windows[0]
        window.activate()
        time.sleep(0.5)  # 等待窗口激活
        return True
    else:
        print("未找到指定的窗口: {0}".format(windowID))
        return False

def home():
    ADBHelper.keyEvent(deviceID, '3')

def back():
    ADBHelper.keyEvent(deviceID, 'KEYCODE_BACK')

def bs_press(bsKeyStr):
    pyautogui.hotkey('ctrl', 'shift', bsKeyStr)
    time.sleep(0.5)

def bs_manager_click(windowID, pos):
    windows = gw.getWindowsWithTitle(windowID)
    x, y = pos
    if windows:
        window = windows[0]
        # 激活窗口
        try: 
            window.activate()
        except Exception:
            # 忽略所有异常
            print("忽略所有异常1")
            # 激活窗口
            try: 
                time.sleep(2)
                window.activate()
            except Exception:
                # 忽略所有异常
                print("忽略所有异常2")
                pass
            pass
        # 首个按钮 150%中 (900, 225), (900, 330), 确认键为 (900, 600)
        button_x = window.left + x
        button_y = window.top + y
        # 移动鼠标并点击按钮
        time.sleep(1.5)
        pyautogui.click(button_x, button_y)
        print("按钮点击成功！")
    else:
        print("未找到窗口，请检查窗口标题。")

def clean_touch(point, times = 1):
    time.sleep(0.5)
    ADBHelper.touch(deviceID, st.empty_block)
    time.sleep(0.5)
    for i in range(times):
        touch(point)
        time.sleep(0.5)

def collect_log_image():
    # 获取当前的日期和时间
    now = datetime.now()
    # 将日期和时间格式化为字符串，例如：20231005_153045
    filename = now.strftime("%Y%m%d_%H%M%S")
    # ADBHelper.screenCapture(deviceID, st.cache_path + f"log_{filename}.png")
    shutil.copy(st.cache_path + "screenCap.png", st.cache_path + f"log_{filename}.png")

def screenCap():
    ADBHelper.screenCapture(deviceID, st.cache_path + "screenCap.png")
    time.sleep(0.1)

def stop_process_by_window_title(window_title):
    # PowerShell命令模板
    ps_command = '''
    Get-Process | Where-Object {{ $_.MainWindowTitle -eq "{0}" }} | Stop-Process -Force
    '''.format(window_title)

    # 使用subprocess运行PowerShell命令
    result = subprocess.run(["powershell", "-Command", ps_command], capture_output=True, text=True)

    # 输出结果
    if result.returncode == 0:
        print(f"成功终止窗口标题为 '{window_title}' 的进程。")
    else:
        print(f"未能终止窗口标题为 '{window_title}' 的进程。错误信息：")
        print(result.stderr)

def run_bluestacks_instance(instance_name):
    # 定义BlueStacks的可执行文件路径
    bluestacks_path = st.player_path

    # 构造完整的命令
    # 直接使用exe地址会导致命令阻塞，窗口若不关闭则result不返回
    # command = f'& "{bluestacks_path}" --instance {instance_name}'
    command = f'Start-Process -FilePath "{bluestacks_path}" -ArgumentList "--instance", "{instance_name}"'
    

    try:
        # 使用subprocess运行命令
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)

        # 检查命令是否成功执行
        if result.returncode == 0:
            print(f"成功启动BlueStacks实例: {instance_name}")
            print("输出:", result.stdout)
        else:
            print(f"启动BlueStacks实例失败: {instance_name}")
            print("错误信息:", result.stderr)
    except Exception as e:
        print(f"运行命令时发生异常: {e}")

# try_screen_capture() as ADBHelper.screenCapture(deviceID, st.cache_path + "screenCap.png")
# def try_screen_capture():
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         # 提交任务
#         future = executor.submit(ADBHelper.screenCapture, deviceID, st.cache_path + "screenCap.png")
#         # 等待任务完成，设置超时时间
#         result = future.result(timeout=timeout)
#         return result
