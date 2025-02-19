#图片匹配置信度，0-1之间，默认0.93，如果匹配出错误目标则提高置信度，如果要模糊匹配或高置信度无法匹配则降低置信度
# accuracy = 0.70
accuracy = 0.60
#正确率0.55时，bubble难以判断
#正确率0.6时，为橘子最佳经验值(有对勾干扰)
#正确率0.75时，可排除bubble
# 0.8用于event

#缓存文件存放地址，以/结尾
cache_path = './cache/'

#随机延时范围[randomDelayMin,randomDelayMax]，单位秒
randomDelayMin = 1
randomDelayMax = 5

#点击偏移范围，[0,x]
touchPosRange = 1

#点击延迟范围，[0,x]
touchDelayRange = 10

#滑屏所需时长范围[slideMinVer,slideMaxVer]，单位毫秒 (滑屏操作不能太快，建议最小值设置在500ms以上)
slideMinVer = 200
slideMaxVer = 300

# blue
# empty_color_1 = (241, 184, 142)
# empty_color_2 = (237, 179, 135)

empty_color_1 = (67, 135, 202)
empty_color_2 = (55, 123, 191)
empty_colors = [empty_color_1, empty_color_2]

# empty_color_green = (185, 183, 88)
# empty_colors = [empty_color_green]
empty_block = (132,576)
event_first_block = (204,736)

