import testDict as rd
deviceList = [
    {"deviceId": '127.0.0.1:5645', "window_title": 'BlueStacks App Main', "instance_title": 'Pie64_9'},
    {"deviceId": '127.0.0.1:5735', "window_title": 'BlueStacks App Save2', "instance_title": 'Pie64_18'},
]

targetListOrangeTree = rd.orange_tree_list1

#图片匹配置信度，0-1之间，默认0.93，如果匹配出错误目标则提高置信度，如果要模糊匹配或高置信度无法匹配则降低置信度
# accuracy = 0.70
accuracy = 0.75
#正确率0.55时，bubble难以判断
#正确率0.6时，为橘子最佳经验值(有对勾干扰)
#正确率0.75时，可排除bubble
# 0.8用于event

#缓存文件存放地址，以/结尾
cache_path = './cache/'
player_path = "C:/Program Files/BlueStacks_nxt/HD-Player.exe"

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

# blue 142-184-241
empty_color_1 = (241, 184, 142)
empty_color_2 = (237, 179, 135)

# brown
# empty_color_1 = (67, 135, 202)
# empty_color_2 = (55, 123, 191)

# green - general Friday
empty_color_1 =  (185, 183, 88)
empty_color_2 = (184, 182, 86)

# deep green
# empty_color_1 =  (114, 139, 66)
# empty_color_2 = (120, 146, 74)

# Spring green
# empty_color_1 =  (96, 181, 125)
# empty_color_2 = (94, 176, 118)

empty_color_1 =  (232, 181, 118)
empty_color_2 = (238, 187, 124)


empty_colors = [empty_color_1, empty_color_2]
empty_block = (132,576)

intoGameList = [
    rd.start_game,
    rd.cloud_button,
    rd.into_board,
    rd.back_from_board
    ]
usePower = True
# usePower = False

# event_first_block 玫瑰 (204,736)
# event_first_block = (685, 1755)

# event_first_block 挖矿 沙滩
event_first_block = (600, 1670)
event_empty_color_1 = (145, 186, 218)
event_empty_color_2 = (134, 172, 207)
# event_empty_block = (132,576)

event_x_start_pos = 136
event_y_start_pos = 668
event_block_size = 68
event_x_line = 6
event_y_line = 8

eventItemList = [
    rd.event_3_a_item_1,
    rd.event_3_a_item_2,
    rd.event_3_a_item_3,
    rd.event_3_a_item_4,
    rd.event_3_a_item_5,
    rd.event_3_a_item_6,
    rd.event_3_a_item_7,
    rd.event_3_a_item_8,
    # rd.event_3_a_item_9,
]

eventTagList = [
    rd.event_3_a_tag_1,
    rd.event_3_a_tag_2,
    rd.event_3_a_tag_3,
    rd.event_3_a_tag_4,
]

eventIntoGameList = [
    rd.start_game,
    rd.cloud_button,
    rd.event_3_a_into,
    rd.event_3_a_at
]

event_empty_colors = [event_empty_color_1, event_empty_color_2]

cardMaxX = 180
cardMaxY = 70