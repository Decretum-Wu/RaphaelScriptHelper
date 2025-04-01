import cv2, numpy

# 从source图片中查找wanted图片所在的位置，当置信度大于accuracy时返回找到的最大置信度位置的左上角坐标
def locate(source, wanted, accuracy=0.90):
    screen_cv2 = cv2.imread(source)
    wanted_cv2 = cv2.imread(wanted)

    result = cv2.matchTemplate(screen_cv2, wanted_cv2, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    print(f"寻找目标图片{wanted}最高相似度：{max_val}")

    if max_val >= accuracy:
        return max_loc
    else:
        return None

# 从source图片中查找wanted图片所在的位置，当置信度大于accuracy时返回找到的所有位置的左上角坐标（自动去重）
def locate_all(source, wanted, accuracy=0.90):
    loc_pos = []
    screen_cv2 = cv2.imread(source)
    wanted_cv2 = cv2.imread(wanted)

    result = cv2.matchTemplate(screen_cv2, wanted_cv2, cv2.TM_CCOEFF_NORMED)
    location = numpy.where(result >= accuracy)

    ex, ey = 0, 0
    for pt in zip(*location[::-1]):
        x = pt[0]
        y = pt[1]

        if abs(x - ex) + abs(y - ey) < 30:  # 去掉邻近重复的点
            continue
        ex, ey = x, y

        loc_pos.append([int(x), int(y)])


    return loc_pos

# 从source图片中查找wanted图片所在的位置，当置信度大于accuracy时返回找到的所有位置的左上角坐标（自动去重）
def locate_all_center(source, wanted, accuracy=0.90):
    loc_pos = []
    screen_cv2 = cv2.imread(source)
    wanted_cv2 = cv2.imread(wanted)

    result = cv2.matchTemplate(screen_cv2, wanted_cv2, cv2.TM_CCOEFF_NORMED)
    location = numpy.where(result >= accuracy)

    ex, ey = 0, 0
    for pt in zip(*location[::-1]):
        x = pt[0]
        y = pt[1]

        if abs(x - ex) + abs(y - ey) < 30:  # 去掉邻近重复的点
            continue
        ex, ey = x, y

        loc_pos.append(centerOfTouchArea(wanted_cv2.shape, (int(x), int(y))))
        # loc_pos.append([int(x), int(y)])

    return loc_pos

# 给定目标尺寸大小和目标左上角顶点坐标，即可给出目标中心的坐标
def centerOfTouchArea(wantedSize, topLeftPos):
    tlx, tly = topLeftPos
    h_src, w_src, tongdao = wantedSize
    if tlx < 0 or tly < 0 or w_src <=0 or h_src <= 0:
        return None
    return (tlx + w_src/2, tly + h_src/2)

def locate_all_center_list(source, wanted_list, accuracy=0.90):
    """
    对于给定的 source 图片和多个 wanted 图片，
    分别在 source 图片中查找每个 wanted 图片的位置，
    返回一个嵌套数组，每个子数组包含对应 wanted 图片在 source 中的中心点坐标列表。
    
    参数：
        source (str): 源图片的路径
        wanted_list (list): 包含多个目标图片路径的列表
        accuracy (float): 匹配精度阈值，默认为 0.90

    返回：
        list: 嵌套列表，每个子列表对应一个 wanted 图片的匹配结果
    """
    # 读取源图片
    screen_cv2 = cv2.imread(source)
    if screen_cv2 is None:
        raise ValueError(f"无法加载源图片：{source}")

    # 用于保存所有 wanted 图片的匹配结果
    results_nested = []

    # 遍历每个 wanted 图片
    for wanted in wanted_list:
        sub_loc_pos = []  # 用于保存当前 wanted 图片的匹配结果
        wanted_cv2 = cv2.imread(wanted)
        if wanted_cv2 is None:
            print(f"警告：无法加载目标图片：{wanted}")
            results_nested.append(sub_loc_pos)
            continue

        # 执行模板匹配
        result = cv2.matchTemplate(screen_cv2, wanted_cv2, cv2.TM_CCOEFF_NORMED)
        location = numpy.where(result >= accuracy)

        # print(f"wanted:{wanted},location:{location}")

        # 记录上一个点的坐标，用于去除过于接近的重复点
        ex, ey = 0, 0
        for pt in zip(*location[::-1]):  # 注意：zip(*location[::-1]) 将得到 (x, y) 坐标对
            x, y = pt[0], pt[1]

            # 若当前点与上一个记录点过于接近（距离和小于 15），则跳过
            if abs(x - ex) + abs(y - ey) < 30:
                continue

            ex, ey = x, y

            # 计算并记录目标区域的中心点，假设 centerOfTouchArea 函数已定义
            center = centerOfTouchArea(wanted_cv2.shape, (int(x), int(y)))
            sub_loc_pos.append(center)

        # 将当前 wanted 图片的匹配结果添加到总结果中
        results_nested.append(sub_loc_pos)

    return results_nested

def get_color(source, position):
    image = cv2.imread(source)
    if image is None:
        raise ValueError("图片读取失败，请检查路径是否正确。")
    x, y = position
    pixel_color = image[y, x]  # OpenCV 中坐标顺序是 (y, x)
    # pixel_color = image[x, y]  # OpenCV 中坐标顺序是 (y, x)
    return pixel_color

def find_matching_coordinates(image_path, coordinates, expected_colors):
    """
    读取图片上指定坐标点的颜色，并输出颜色在 expected_colors 列表中的坐标列表。

    :param image_path: 图片路径
    :param coordinates: 坐标列表，格式为 [(x1, y1), (x2, y2), ...]
    :param expected_colors: 期望的颜色值列表，格式为 [(B1, G1, R1), (B2, G2, R2), ...]
    :return: 颜色匹配的坐标列表
    """
    # 读取图片
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("图片读取失败，请检查路径是否正确。")

    # 将 expected_colors 转换为 NumPy 数组以便比较
    expected_colors = numpy.array(expected_colors)

    # 初始化结果列表
    matching_coordinates = []

    # 遍历坐标列表
    for (x, y) in coordinates:
        # 读取坐标点的颜色
        pixel_color = image[y, x]  # OpenCV 中坐标顺序是 (y, x)
        # pixel_color = image[x, y]  # OpenCV 中坐标顺序是 (y, x)

        # 检查颜色是否在 expected_colors 中
        if any(numpy.array_equal(pixel_color, color) for color in expected_colors):
            matching_coordinates.append((x, y))

    return matching_coordinates

def get_color_list(image_path, coordinates):
    """
    读取图片上指定坐标点的颜色

    :param image_path: 图片路径
    :param coordinates: 坐标列表，格式为 [(x1, y1), (x2, y2), ...]
    :param expected_colors: 期望的颜色值列表，格式为 [(B1, G1, R1), (B2, G2, R2), ...]
    :return: 颜色匹配的坐标列表
    """
    # 读取图片
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("图片读取失败，请检查路径是否正确。")


    # 初始化结果列表
    result = []

    # 遍历坐标列表
    for (x, y) in coordinates:
        # 读取坐标点的颜色
        pixel_color = image[y, x]  # OpenCV 中坐标顺序是 (y, x)
        # pixel_color = image[x, y]  # OpenCV 中坐标顺序是 (y, x)

        result.append(pixel_color)

    return result