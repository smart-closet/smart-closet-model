import csv
import time
from lib.df1 import DeepFashion1Model
from PIL import Image
import os
import google.generativeai as genai
from dotenv import load_dotenv

df1_model = DeepFashion1Model()

# Set up Gemini API
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# define prompt
prompt = """Please examine the following images and identify the types of clothing they contain. For each image, only list the types from the following list, output them in order, separated by commas:

t-shirt
shirt
dress-shirt
button-up-shirt
flannel-shirt
sweater
hoodie
jacket
coat
trench-coat
suit-jacket
denim-jacket
leather-jacket
polo-shirt
knit-top
vest
sweater-vest
tank-top
turtleneck
dress
skirt
long-skirt
pants
jeans
shorts
suit-pants
yoga-pants
sweatpants
overalls
jumpsuit
pajamas
bathrobe
cotton-pants
wool-pants
leggings
windproof-pants
cotton-vest
down-jacket
ski-jacket
cotton-coat
thermal-underwear
padded-jacket
winter-sportswear
insulated-vest
thick-jeans
college-sweatshirt

Format example: 
Image 1: t-shirt, jeans, hoodie
Image 2: sweater, pants, jacket
...

Please start identifying and listing the types of clothing in each image:
"""

# Define folder paths and output CSV file
output_csv = "fashion_results_.csv"
data_path = "data_raw"

def process_batch(batch, writer):
    images = []
    for img_path, folder, filename in batch:
        img = Image.open(img_path).convert("RGB")
        images.append(img)

    try:
        response = model.generate_content([prompt] + images)
        gemini_results = response.text.strip().split('\n')

        for i, (img_path, folder, filename) in enumerate(batch):
            img = Image.open(img_path).convert("RGB")
            df1_tags = df1_model.infer(img, 0.13)
            
            gemini_tags = gemini_results[i].split(': ')[1].split(', ') if i < len(gemini_results) else []
            
            tags = list(set(df1_tags + gemini_tags))
            writer.writerow([folder.replace("cut_", ""), filename, ",".join(tags)])
            print(f"已處理 {img_path}")
    except Exception as e:
        print(f"處理批次時發生錯誤: {str(e)}")
        for img_path, _, _ in batch:
            print(f"處理失敗: {img_path}")

# Open CSV file for writing
with open(output_csv, mode="a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["folder", "filename", "tags"])

    # Process each image in the folders
    for folder in sorted(os.listdir(data_path)):
        folder_path = os.path.join(data_path, folder)
        if "style" not in folder:
            continue
        print(f"處理文件夾: {folder}")
        print("==================================================================================\n")

        # 讀取已處理的圖片列表
        processed_images = set()
        with open(output_csv, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # 跳過標題行
            for row in reader:
                if row[0] == folder.replace("cut_", ""):
                    processed_images.add(row[1])
        
        # 過濾掉已處理的圖片
        files = sorted([f for f in os.listdir(folder_path) if f not in processed_images])
        total_files = len(files)
        processed_count = 0
        
        batch = []
        for filename in files:
            if filename.endswith((".jpg", ".jpeg")):
                img_path = os.path.join(folder_path, filename)
                batch.append((img_path, folder, filename))
                
                if len(batch) == 1:
                    process_batch(batch, writer)
                    processed_count += len(batch)
                    batch = []
                    remaining = total_files - processed_count
                    print(f"進度: {processed_count}/{total_files} 已處理，剩餘 {remaining} 張")
                    time.sleep(1)
        
        # 處理剩餘的圖片
        if batch:
            process_batch(batch, writer)
            processed_count += len(batch)
            remaining = total_files - processed_count
            print(f"進度: {processed_count}/{total_files} 已處理，剩餘 {remaining} 張")

        print(f"文件夾 {folder} 處理完成，共處理 {processed_count} 張圖片")
        print("==================================================================================\n")

print(f"結果已寫入 {output_csv}")