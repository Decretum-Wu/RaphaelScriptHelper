import logging
import RaphaelScriptHelper as gamer
import settings as st

def get_center(grid_pos):
    if grid_pos is None:
        return None
    row, col = grid_pos
    x = 64 + (col - 1) * 136 + 68  # 计算x坐标：起点64 + (列数-1)*格子宽度 + 半宽
    y = 508 + (row - 1) * 136 + 68  # 计算y坐标：起点508 + (行数-1)*格子高度 + 半高
    return (x, y)

def get_all_center():
    resultList = []
    for col in range(1,8):
        for row in range(1,10):
            x = 64 + (col - 1) * 136 + 68  # 计算x坐标：起点64 + (列数-1)*格子宽度 + 半宽
            y = 508 + (row - 1) * 136 + 68  # 计算y坐标：起点508 + (行数-1)*格子高度 + 半高
            resultList.append((x,y))
    return resultList

def get_grid_pos(screen_pos):
    x, y = screen_pos
    # 计算列号（横向格子）
    col = (x - 64) // 136 + 1
    # 计算行号（纵向格子）
    row = (y - 508) // 136 + 1
    # 检查是否在棋盘有效范围内
    if 1 <= col <= 7 and 1 <= row <= 9:
        return (row, col)
    else:
        return None  # 坐标不在棋盘格子上

def get_unique_grid_positions(coords_list):
    # 定义集合存储唯一的有效棋盘位置
    unique_positions = set()
    
    for screen_coord in coords_list:
        grid_pos = get_grid_pos(screen_coord)  # 复用之前的坐标转换函数
        grid_center_pos = get_center(grid_pos)
        if grid_center_pos is not None:  # 过滤无效坐标
            # 将位置转换为元组并存入集合（自动去重）
            unique_positions.add(grid_center_pos)
    
    # 将集合转为有序列表（按行号、列号升序排列）
    return sorted(unique_positions, key=lambda x: (x[0], x[1]))

def read_list_to_unique_grid_positions(read_list):
    # 定义集合存储唯一的有效棋盘位置
    unique_positions = set()
    
    for grid_pos in read_list:
        grid_center_pos = get_center(grid_pos)
        if grid_center_pos is not None:  # 过滤无效坐标
            # 将位置转换为元组并存入集合（自动去重）
            unique_positions.add(grid_center_pos)
    
    # 将集合转为有序列表（按行号、列号升序排列）
    return sorted(unique_positions, key=lambda x: (x[0], x[1]))

def get_unique_grid_positions_read(coords_list):
    # 定义集合存储唯一的有效棋盘位置
    unique_positions = set()
    
    for screen_coord in coords_list:
        grid_pos = get_grid_pos(screen_coord)  # 复用之前的坐标转换函数
        if grid_pos is not None:  # 过滤无效坐标
            # 将位置转换为元组并存入集合（自动去重）
            unique_positions.add(grid_pos)
    
    # 将集合转为有序列表（按行号、列号升序排列）
    return sorted(unique_positions, key=lambda x: (x[0], x[1]))

def process_unique_positions_col(unique_positions_col):
    seen = set()
    processed_temp = []
    
    # 倒序遍历每个列表（按原索引从后往前）
    for idx in reversed(range(len(unique_positions_col))):
        current_list = unique_positions_col[idx]
        new_list = []
        for elem in current_list:
            if elem in seen:
                print(f"元素{elem}在后面的列表中被覆盖，已从列表{idx}中移除")
            else:
                new_list.append(elem)
                seen.add(elem)
        processed_temp.append(new_list)
    
    # 反转结果恢复原顺序
    return processed_temp[::-1]

def get_collection_unique_grid_positions(coords_col):
    unique_positions_col = []
    for coords_list in coords_col:
        unique_positions_col.append(get_unique_grid_positions(coords_list))
    unique_positions_col = process_unique_positions_col(unique_positions_col)
    return unique_positions_col

def get_collection_unique_grid_positions_read(coords_col):
    unique_positions_col = []
    for coords_list in coords_col:
        unique_positions_col.append(get_unique_grid_positions_read(coords_list))
    return unique_positions_col

def process_collection(collection, merge_func):
    """
    处理嵌套列表集合，按新规则合并并传递元素
    :param collection: 顺序排列的列表集合（原地修改）
    :param merge_func: 合并函数，返回两个元素中的前者
    :return: 总合并操作次数
    """
    logging.basicConfig(level=logging.INFO,
                       format='%(asctime)s - %(levelname)s: %(message)s')
    total_merges = 0

    for list_idx in range(len(collection)):
        current_list = collection[list_idx]
        
        # 跳过无效列表记录
        if len(current_list) < 2:
            status = "empty" if not current_list else "single-element"
            logging.info(f"List {list_idx} ({status}) skipped")
            continue

        merged_results = []
        # 持续处理直到剩余元素不足两个
        while len(current_list) >= 2:
            # 总是取出前两个元素
            a = current_list.pop(0)
            b = current_list.pop(0)
            merged_results.append(merge_func(a, b))
            total_merges += 1
            gamer.delay(0.1)
            # 实时日志
            logging.debug(f"Merged ({a}, {b}) in list {list_idx}")

        # 将结果传递到下一层（如果有）
        if list_idx < len(collection) - 1:
            next_list = collection[list_idx+1]
            next_list.extend(merged_results)
            logging.info(f"Added {len(merged_results)} elements to list {list_idx+1}")

    # 最终统计输出
    logging.info(f"TOTAL MERGE OPERATIONS: {total_merges}")
    return total_merges

def find_item_counts(targetPic):
    return len(get_collection_unique_grid_positions(gamer.find_pic_all_list([targetPic]))[0])

# TODO, find_pic_all_list需要支持cache
def find_board_items(targetPic, accuracy = st.accuracy, cacheFlag = False):
    return get_collection_unique_grid_positions(gamer.find_pic_all_list([targetPic], accuracy))[0]

def stable_find_board_items(targetPic, retryCount = 1, accuracy = st.accuracy, cacheFlag = False):
    # gamer.delay(1.5)
    resourceList = []
    for i in range(retryCount):
        resourceList = find_board_items(targetPic, accuracy, cacheFlag)
        # gamer.delay(1)
        if len(resourceList) > 0:
            break
    return resourceList

def combine_lists_to_dict(keyList, valueList):
    # 检查两个列表长度是否一致
    if len(keyList) != len(valueList):
        raise ValueError("两个列表长度不同，无法合并为键值对")
    # 使用 zip 合并为字典
    return dict(zip(keyList, valueList))

def click_order(targetPic):
    tempList = gamer.find_pic_all_list([targetPic])[0]
    if len(tempList) > 0:
        point = tempList[0]
        x, y = point
        gamer.touch((x,y - 70))
        print(f"成功点击{targetPic}")
    else:
        print(f"未能点击{targetPic}")

def calculate_total_weight(collection):
    total_weight = 0
    for index, lst in enumerate(collection):
        weight = 2 ** index  # 计算当前列表的权重
        total_weight += len(lst) * weight  # 当前列表的总权重 = 列表长度 * 权重
    return total_weight

def get_total_weight(collection, accuracy = st.accuracy):
    return calculate_total_weight(get_collection_unique_grid_positions(gamer.find_pic_all_list(collection, accuracy)))



# TODO: 新的清理棋盘逻辑
# 对每个待处理LIST的第一个元素进行扫描，如果发现长度大于2则合成
# 返回合成的index位置，用于进一步对整个list进行清理
# 如果有orange因此被合成，进行完整orange逻辑


# def process_collection(collection, merge_func):
#     """
#     处理嵌套列表集合，按新规则合并并传递元素
#     :param collection: 顺序排列的列表集合（原地修改）
#     :param merge_func: 合并函数，返回两个元素中的前者
#     :return: 总合并操作次数
#     """
#     logging.basicConfig(level=logging.INFO,
#                        format='%(asctime)s - %(levelname)s: %(message)s')
#     total_merges = 0

#     for list_idx in range(len(collection)):
#         current_list = collection[list_idx]
        
#         # 跳过无效列表记录
#         if len(current_list) < 2:
#             status = "empty" if not current_list else "single-element"
#             logging.info(f"List {list_idx} ({status}) skipped")
#             continue

#         merged_results = []
#         # 持续处理直到剩余元素不足两个
#         while len(current_list) >= 2:
#             # 总是取出前两个元素
#             a = current_list.pop(0)
#             b = current_list.pop(0)
#             merged_results.append(merge_func(a, b))
#             total_merges += 1
#             gamer.delay(0.1)
#             # 实时日志
#             logging.debug(f"Merged ({a}, {b}) in list {list_idx}")

#         # 将结果传递到下一层（如果有）
#         if list_idx < len(collection) - 1:
#             next_list = collection[list_idx+1]
#             next_list.extend(merged_results)
#             logging.info(f"Added {len(merged_results)} elements to list {list_idx+1}")

#     # 最终统计输出
#     logging.info(f"TOTAL MERGE OPERATIONS: {total_merges}")
#     return total_merges

# def clean_up(type):
#     if type == 1:
#         morning_clean()
#         process_existed(targetListCoin, True)
#         #temp
#         process_existed(targetListPower, True)
#         process_existed_orange()
#         # process_existed(targetListStone)
#         # gamer.find_pic_double_touch(rd.stone_4)

#         # process_existed(targetListBlue)
#         gamer.delay(1)
#     elif type == 2: 
#         clean_up(1)
#         # process_existed(targetListFloat)
#         gamer.delay(1)
#         gamer.find_pic_double_touch(rd.coin_new_5)
#         gamer.find_pic_double_touch(rd.coin_new_4)
#         # gamer.find_pic_double_touch(rd.float_4)
#     else:
#         clean_up(2)
#         # gamer.find_pic_double_touch(rd.icon_4)
#         gamer.find_pic_double_touch(rd.coin_new_3)
#         gamer.find_pic_double_touch(rd.coin_new_2)
#         gamer.find_pic_double_touch(rd.coin_new_1)

# def verify_clean(minNum = 1):
#     count = len(gamer.find_all_empty(ghh.get_all_center()))
#     initCount = count
#     # 一个格子时，空格数大于0
#     minNum = minNum - 1
#     clean_up(1)
#     gamer.delay(0.5)
#     count = len(gamer.find_all_empty(ghh.get_all_center()))
#     # if not (count > minNum):
#     #     clean_up(1)
#     #     count = len(gamer.find_all_empty(ghh.get_all_center()))
#     #     logging.info(msh.send_simple_push(f"检测到棋盘满,剩余空格数{count}",f"提示：一级清理,剩余空格数{count}"))
#     if not (count > minNum):
#         if useCoin:
#             clean_up(2)
#             gamer.delay(0.5)
#             count = len(gamer.find_all_empty(ghh.get_all_center()))
#             logging.info(msh.send_simple_push(f"检测到棋盘满,剩余空格数{count}",f"提示：二级清理,剩余空格数{count}"))
#         else:
#             logging.info(msh.send_simple_push(f"检测到棋盘满,剩余空格数{count}",f"提示：二级清理,不能使用金币，暂停"))
#     if not (count > minNum):
#         if useCoin:
#             clean_up(3)
#             process_existed_orange()
#             # process_existed_orange()
#             # process_existed_orange()
#             # process_existed_orange()
#             # process_existed_orange()
#             gamer.delay(0.5)
#             count = len(gamer.find_all_empty(ghh.get_all_center()))
#             logging.info(msh.send_simple_push(f"检测到棋盘满,剩余空格数{count}",f"提示：三级清理,剩余空格数{count}"))
#         else:
#             logging.info(msh.send_simple_push(f"检测到棋盘满,剩余空格数{count}",f"提示：三级清理,不能使用金币，暂停"))
#     if not (count > minNum):
#         gamer.collect_log_image("清理棋盘失败")
#         gamer.delay(1200)
#         return False
#     else:
#         # 如果清理过 save
#         if count > initCount:
#             gamer.home()
#             time.sleep(3)
#             gamer.find_pic_touch(rd.start_game)
#         return True
    
