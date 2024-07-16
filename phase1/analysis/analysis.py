import csv
from lib.df2 import DeepFashion2Model
from lib.df1 import DeepFashion1Model
from PIL import Image
import numpy as np
import cv2
import os

df1_model = DeepFashion1Model()
df2_model = DeepFashion2Model()

# Define folder path and output CSV file
output_csv = "fashion_results.csv"
data_path = "data"

# Open CSV file for writing
with open(output_csv, mode='a', newline='') as file:
    writer = csv.writer(file)
    # writer.writerow(["folder", "filename", "tags"])

    # Process each image in the folder
    for folder in sorted(os.listdir(data_path)):
        folder_path = os.path.join(data_path, folder)
        if ("style" not in folder):
            print(f"pass {folder}")
            continue
        print(f"Processing {folder}")
        print("==================================================================================\n")
        
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                img_path = os.path.join(folder_path, filename)
                img = Image.open(img_path).convert("RGB")
                tags = df1_model.infer(img, 0.13)
                tags.append(df2_model.infer(cv2.imread(img_path)))
                writer.writerow([folder.replace("cut_", ""), filename, ','.join(tags)])
                print(f"Processing {img_path}")
        
print(f"Results written to {output_csv}")
