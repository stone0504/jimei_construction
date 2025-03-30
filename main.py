import requests
import time
from bs4 import BeautifulSoup
import hashlib
import datetime
import screenshot
import os
from pathlib import Path
import json
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo  # type: ignore for VS Code

config_path = Path(__file__).parent / "config.json"
with config_path.open() as f:
    config = json.load(f)


# === LINE API 設定 ===
LINE_ACCESS_TOKEN = config["LINE_ACCESS_TOKEN"]
USER_ID = config["USER_ID"] # piccc group
LINE_API_URL = config["USER_ID"]

# === 目標網址與 session 設定 ===
homepage_url = config["homepage_url"]  # 首頁，先訪問以建立 session
target_url = config["target_url"]  # 目標頁面
check_interval = 7200  # 每 7200 小時檢查一次 （7200）


# 本机图片路径
IMAGE_PATH = screenshot.screenshot_path

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
}

def send_message():
    data = {
        "to": USER_ID,
        "messages": [
            {
                "type": "text",
                "text": "森城網頁有新更新！請查看系統。\nhttp://www.sccoltd.com.tw/in-progress/123"
            }
        ]
    }
    response = requests.post(LINE_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        print("訊息發送成功！")
    else:
        print(f"發送失敗，錯誤代碼：{response.status_code}")
        print(response.text)

def send_image():
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
    }

    # 先上传图片到外部服务器（因为 LINE API 需要图片的 URL）
    image_url = upload_image_to_imgur(IMAGE_PATH)

    if not image_url:
        print("图片上传失败")
        return

    # 发送消息
    payload = {
        "to": USER_ID,
        "messages": [
            {
                "type": "image",
                "originalContentUrl": image_url,  # 图片的 URL
                "previewImageUrl": image_url,  # 预览图的 URL
            }
        ],
    }

    response = requests.post(LINE_API_URL, json=payload, headers=headers)
    print(response.json())

# 使用 Imgur API 上传图片（或你自己的图床）
def upload_image_to_imgur(image_path):
    IMGUR_CLIENT_ID = config["IMGUR_CLIENT_ID"]  # 需要去 Imgur 申请
    headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
    with open(image_path, "rb") as f:
        files = {"image": f}
        response = requests.post("https://api.imgur.com/3/upload", headers=headers, files=files)

    if response.status_code == 200:
        return response.json()["data"]["link"]
    else:
        print("图片上传失败:", response.json())
        return None


# === 取得網頁內容並計算 Hash ===
def get_page_content():
    with requests.Session() as session:
        # 先訪問首頁以建立 session
        session.get(homepage_url)
        
        # 訪問目標網頁
        response = session.get(target_url)
        
        if response.status_code != 200:
            print(f"請求失敗，錯誤代碼：{response.status_code}")
            return ""

        soup = BeautifulSoup(response.text, 'html.parser')

        # 找出網頁內的主要內容
        main_content = soup.find("table")  # 你可以改成特定的 `div` 或 `section`
        
        return main_content.text.strip() if main_content else ""

def get_content_hash(content):
    return hashlib.md5(content.encode()).hexdigest()

def now_time():
    now_utc = datetime.datetime.now(ZoneInfo("UTC"))
    taipei_time = now_utc.astimezone(ZoneInfo("Asia/Taipei"))
    return taipei_time.strftime("%Y-%m-%d %H:%M:%S")

previous_hash = ""

while True:
    try:
        page_content = get_page_content()
        current_hash = get_content_hash(page_content)

        if previous_hash and current_hash != previous_hash:
            print(f"{now_time()}: 網頁有更新！")
            screenshot.screenshot()
            send_message()
            send_image()
            time.sleep(3)
            os.remove(IMAGE_PATH)
        else:
            print(f"{now_time()}: 沒有變更")
            '''
            screenshot.screenshot()
            send_message()
            send_image()
            time.sleep(3)
            os.remove(IMAGE_PATH)
            '''
        previous_hash = current_hash
        time.sleep(check_interval)

    
    
    except Exception as e:
        print(f"ERROR: {e}")
        time.sleep(check_interval)
