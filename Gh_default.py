
# 请参考视频教程 https://www.bilibili.com/video/BV1u3411E7KD/ 改写此脚本后再运行
# 请注意视频教程或文字教程中的相关注意事项

import RaphaelScriptHelper as gamer
import multiprocessing
import testDict as rd
import settings
from enum import Enum

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

# 请在跑脚本之前参考教程修改这一部分
# =======================================================================

# 安卓设备的DID
gamer.deviceID = "emulator-5554"
# gamer.deviceID = "emulator-5574"

# 测试用
tempList = gamer.find_pic_all(rd.orange_2_a)
print("获取橘子位置，首个点为 {0} ，实际数量  {1}".format(tempList[0] if (len(tempList) > 0) else "", len(tempList)))

if len(tempList) > 1:
    gamer.slide((tempList[1], tempList[0]))

tempList = gamer.find_pic_all(rd.orange_4_a)
print("获取橘子文本位置，首个点为 {0} ，实际数量  {1}".format(tempList[0] if (len(tempList) > 0) else "", len(tempList)))

# 1 寻找对应中心点
# 2 判断数量是否大于2，如果是
# 3 拖动方法
# 4 循环判断
# 250127 tips, 部分成功，但1寻图逻辑需要优化，多图同时寻+处理
# 2 需要识图判断橘子树状态，挪开占位物品(难)

# TODO 完成体力箱识别，以及保存功能 
while True:
    tempList = gamer.find_pic_all(rd.orange_1_a)
    if len(tempList) > 1:
        for i in range(0,len(tempList) - 1,2):
            gamer.slide((tempList[i+1], tempList[i]))
        continue
    tempList = gamer.find_pic_all(rd.orange_2_a)
    if len(tempList) > 1:
        for i in range(0,len(tempList) - 1,2):
            gamer.slide((tempList[i+1], tempList[i]))
        continue
    tempList = gamer.find_pic_all(rd.orange_3_a)
    if len(tempList) > 1:
        for i in range(0,len(tempList) - 1,2):
            gamer.slide((tempList[i+1], tempList[i]))
        continue
    tempList = gamer.find_pic_all(rd.orange_4_a)
    if len(tempList) > 1:
        for i in range(0,len(tempList) - 1,2):
            gamer.slide((tempList[i+1], tempList[i]))
        continue
    tempList = gamer.find_pic_all(rd.orange_5_a)
    if len(tempList) > 1:
        for i in range(0,len(tempList) - 1,2):
            gamer.slide((tempList[i+1], tempList[i]))
        continue
    tempList = gamer.find_pic_all(rd.orange_6_a)
    if len(tempList) > 1:
        for i in range(0,len(tempList) - 1,2):
            gamer.slide((tempList[i+1], tempList[i]))
        continue
