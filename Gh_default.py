
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

# 测试用
tempList = gamer.find_pic_all(rd.orange_3_a)
print("获取橘子位置，首个点为 {0} ，实际数量  {1}".format(tempList[0] if (len(tempList) > 0) else "", len(tempList)))
tempList = gamer.find_pic_all(rd.orange_3_b)
print("获取橘子文本位置，首个点为 {0} ，实际数量  {1}".format(tempList[0] if (len(tempList) > 0) else "", len(tempList)))
