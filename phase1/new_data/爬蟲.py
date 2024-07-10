import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import urllib.request
from PIL import Image

# 啟動 Chrome 瀏覽器
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
count_per_page = 60
total_pages = 30  # 總頁數
path = "occasion:conference"

# 創建保存圖片的目錄
os.makedirs(path, exist_ok=True)

image_count = 0

for page in range(1, total_pages + 1):
    url = f"https://wear.tw/category/tops/?tag_ids=2475&user_type=1&suggest_flag=1&pageno={page}"
    driver.get(url)
    
    # 等待一些時間讓網頁加載完成
    time.sleep(3)
    
    # 網頁捲動，確保所有內容都被加載出來
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        if len(driver.find_elements(By.XPATH, "//img")) > count_per_page * 2:
            break

    # 找到所有衣服圖片的元素
    clothes_images = driver.find_elements(By.XPATH, "//img")

    for idx, img in enumerate(clothes_images):
        if image_count >= count_per_page * page:
            break
        
        img_url = img.get_attribute("src")
        if img_url and img_url.startswith("http"):
            img_name = f"{image_count + 1}.jpg"
            img_path = os.path.join(path, img_name)
            
            # 下載圖片
            try:
                urllib.request.urlretrieve(img_url, img_path)
                
                # 檢查圖片尺寸
                with Image.open(img_path) as img_file:
                    width, height = img_file.size
                    if width < 250 or height < 250:
                        print(f"Skipping {img_name} - Image size too small ({width}x{height})")
                        os.remove(img_path)  # 刪除尺寸太小的圖片檔案
                        continue
                    else:
                        image_count += 1
                        print(f"Downloaded {img_name}")
                
            except Exception as e:
                print(f"Failed to download {img_name}: {e}")
                continue

# 關閉瀏覽器
driver.quit()
