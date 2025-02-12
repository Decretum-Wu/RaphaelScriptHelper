## 简介
项目结构 GossipHabor内其他py文件为资源文件，

get_all_center 存在潜在bug, range不正确？
find_first_resource_point 有潜在bug, 数量不正确


for pt in zip(*location[::-1]) 尝试sorted

潜在问题4 单大屏时点击位置不正确，需要重新计算分辨率

返回键 + 点击屏幕顶部
返回键点击后可能回到首屏

PyAutoGUI fail-safe triggered from mouse moving to a corner of the screen. To disable this fail-safe, set pyautogui.FAILSAFE to False. DISABLING FAIL-SAFE IS NOT RECOMMENDED.


2025-02-12 02:09:58,997 - INFO: 在第71次执行中，目标物列表: []
2025-02-12 02:09:59,346 - INFO: 切换至设备127.0.0.1:5625
函数 screenCapture 运行超时（12 秒）
[100%] sdcard/adb_screenCap.png
忽略所有异常1
忽略所有异常2
按钮点击成功！

检测到超时后，似乎因为等待函数返回而为切断等待，导致catch未能及时触发

通过云端数据后等待实现有人介入的暂停

不稳定要素：需检测双设备是否已经启动
