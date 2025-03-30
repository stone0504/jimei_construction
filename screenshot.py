from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from pathlib import Path
import json
screenshot_path = Path(__file__).parent / "screenshot.png"

config_path = Path(__file__).parent / "config.json"
with config_path.open() as f:
    config = json.load(f)
    
homepage_url = config["homepage_url"]  # 首頁，先訪問以建立 session
target_url = config["target_url"]  # 目標頁面

def screenshot():
    options = Options()
    options.add_argument("--headless")  # 無頭模式
    options.add_argument("--no-sandbox")  # 避免權限問題
    options.add_argument("--disable-dev-shm-usage")  # 避免資源不足
    options.add_argument("--disable-gpu")  # 某些系統需要這個
    options.add_argument("--window-size=800x600")  # 設定解析度

    # 啟動瀏覽器
    driver = webdriver.Chrome(options=options)

    # 先訪問首頁，讓 Session 建立
    driver.get(homepage_url)
    print("Waiting for session to establish...")
    time.sleep(2)  # 等待 2 秒確保 session 建立

    # 再跳轉到目標頁面
    driver.get(target_url)
    print("Navigated to target page, waiting for it to load...")
    time.sleep(2)  # 等待 2 秒確保頁面載入完整
    '''
    # 滾動到頁面底部
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("Scrolling to the bottom...")
    time.sleep(3)  # 等待 3 秒確保頁面完全載入
    '''
    # 截取整個頁面
    
    driver.save_screenshot(screenshot_path)
    print("Screenshot saved as 'screenshot.png'")

    # 關閉瀏覽器
    driver.quit()
if __name__ == '__main__':
    screenshot()
