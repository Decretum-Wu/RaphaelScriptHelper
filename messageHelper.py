import requests
import json

def send_simple_push(content, summary, content_type = 1, spt='SPT_tTVsZ8EgHWY5D0ibTUNVV1799p41'):
    """
    发送极简推送消息

    :param content: 推送内容（必传）
    :param summary: 消息摘要（可选）
    :param content_type: 内容类型（1: 文字, 2: HTML, 3: Markdown）
    :param spt: 发送给单个用户的 simplePushToken
    :return: 请求响应
    """
    # 请求URL
    url = "https://wxpusher.zjiecode.com/api/send/message/simple-push"

    # 请求头
    headers = {
        "Content-Type": "application/json"
    }

    # 请求体
    payload = {
        "content": content,
        "summary": summary,
        "contentType": content_type,
        "spt": spt
    }

    # 发送POST请求
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # 返回响应
    return response.json()