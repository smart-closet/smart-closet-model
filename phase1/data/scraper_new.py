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
count = 1000

# 前往目標網站
# url = "https://www.google.com/search?q=%E9%9F%93%E9%A2%A8+%E7%A9%BF%E6%90%AD+%E5%A5%B3&sca_esv=0119435a3a07c38d&udm=2&biw=1920&bih=1136&sxsrf=ADLYWIJpWyoqMPexBrKX1SM-j4hI6-FP8Q:1719241057785&ei=YYl5ZujCL_Tn1e8P1K-FqAc&oq=%E9%9F%93%E9%A2%A8+%E7%A9%BF%E6%90%AD&gs_lp=Egxnd3Mtd2l6LXNlcnAiDemfk-miqCDnqb_mkK0qAggCMgUQABiABDIFEAAYgAQyBRAAGIAESMMRUABYAHABeACQAQCYAQCgAQCqAQC4AQHIAQCYAgGgAgOYAwCIBgGSBwExoAcA&sclient=gws-wiz-serp"
# path = "korean"

# url = "https://www.google.com/search?sca_esv=19d77d7eb1863703&rlz=1C5CHFA_enTW1077TW1077&sxsrf=ADLYWIIcfDT7-T8EGnRK9Qun7Wy2ahrU2g:1718733843473&q=uniqlo+%E7%A9%BF+%E6%90%AD+%E5%A5%B3+%E5%A4%8F%E5%A4%A9&uds=ADvngMgm7pifeiF9EHlwODIzlHamb6SYxJ9zg_10gszEhQSLbQJCIyDKHAdGJwGz55hHMy-g0u-Jg-QZyrTg0MshS1pLTePj6gr6N2yYYXQu8K9mNzNk-qIQasux5d55dY2c2tNaVFfsKI6Y8JP09TJ-0ZG_E2RKdcGJ4uDJfFEdt1d-18y7yMsBY_d4UXtCDNMG6Yw7WM-28Fc01zMy49kgnnhUO9JWiA&udm=2&sa=X&ved=2ahUKEwjJmtDB3uWGAxWwcPUHHdxMALEQxKsJegQIChAB&ictx=0&biw=1920&bih=934&dpr=1#vhid=0B_V0olOfvHzcM&vssid=mosaic"
# path = "japanese"

url = "https://www.google.com/search?q=%E6%AD%90%E7%BE%8E%E9%A2%A8+%E7%A9%BF%E6%90%AD+%E5%A5%B3&sca_esv=19d77d7eb1863703&rlz=1C5CHFA_enTW1077TW1077&udm=2&biw=1440&bih=836&sxsrf=ADLYWIIrVBWWhxwCBbzk6Sje6KbFSf_dLA:1719269512516&ei=iPh5ZpKdH9LBvr0PsOKB0A4&ved=0ahUKEwiSgcSEqvWGAxXSoK8BHTBxAOoQ4dUDCBA&uact=5&oq=%E6%AD%90%E7%BE%8E%E9%A2%A8+%E7%A9%BF%E6%90%AD+%E5%A5%B3&gs_lp=Egxnd3Mtd2l6LXNlcnAiFOatkOe-jumiqCDnqb_mkK0g5aWzSPcLUHJY2QZwAXgAkAEAmAFvoAGgA6oBAzEuM7gBA8gBAPgBAZgCAqACcMICBRAAGIAEwgIEEAAYHpgDAIgGAZIHAzEuMaAH5wE&sclient=gws-wiz-serp"
path = "american"
driver.get(url)

# 等待一些時間讓網頁加載完成
time.sleep(3)

# 網頁捲動，確保所有內容都被加載出來
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    print(len(driver.find_elements(By.XPATH, "//img")))
    if len(driver.find_elements(By.XPATH, "//img")) > count * 2:
        break

# 找到所有衣服圖片的元素
clothes_images = driver.find_elements(By.XPATH, "//img")

# 創建保存圖片的目錄
os.makedirs(path, exist_ok=True)

image_count = 0
for idx, img in enumerate(clothes_images):
    if image_count >= count:
        break
    
    img_url = img.get_attribute("src")
    if img_url and img_url.startswith("http"):
        img_name = f"{image_count}.jpg"
        img_path = os.path.join(path, img_name)
        
        # 下載圖片
        try:
            urllib.request.urlretrieve(img_url, img_path)
            
            # 檢查圖片尺寸
            with Image.open(img_path) as img_file:
                width, height = img_file.size
                if width < 100 or height < 100:
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
