import os
from dotenv import load_dotenv
import cv2
import glob
from PIL import Image
from inference_sdk import InferenceHTTPClient
import supervision as sv


class DeepFashion2Model:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("API_KEY")
        if api_key is None:
            raise ValueError("API_KEY is not set. Please check your .env file.")
        print(f"Using API_KEY: {api_key}")  # 確認 API 金鑰已被載入
        self.model = InferenceHTTPClient(
            api_url="https://detect.roboflow.com", api_key=api_key
        )
    
    def infer(self, image):
        results = self.model.infer(image, model_id="deepfashion2-m-10k/2")
        if results is None:
            print("No results returned from inference.")
            return []
        
        detections = sv.Detections.from_inference(results)

        if detections.mask is None:
            print("No masks found in detections.")
            return []

        def extract_clean_clothing_with_mask(image, mask):
            mask = mask.astype('uint8') * 255
            clean_clothing_region = cv2.bitwise_and(image, image, mask=mask)
            clean_clothing_region = Image.fromarray(cv2.cvtColor(clean_clothing_region, cv2.COLOR_BGR2RGB))
            return clean_clothing_region

        clean_clothing_images = []
        for i, mask in enumerate(detections.mask):
            clean_clothing_region = extract_clean_clothing_with_mask(image, mask)
            clean_clothing_images.append({
                "clean_clothing_region": clean_clothing_region,
                "classes": detections.data["class_name"][i],
            })
        
        return clean_clothing_images

def get_output_path(base_output_path, suffix, ext):
    counter = 0
    output_path = f"{base_output_path}_{suffix}{ext}"
    while os.path.exists(output_path):
        counter += 1
        output_path = f"{base_output_path}_{suffix}_{counter}{ext}"
    return output_path

def process_folder(input_folder, output_folder):
    # 確保輸出資料夾存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 初始化模型
    model = DeepFashion2Model()

    # 取得所有圖片文件
    image_paths = glob.glob(os.path.join(input_folder, "*.*"))

    # 初始化計數器
    class_count = {}

    for image_path in image_paths:
        # 讀取圖片
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error reading image {image_path}")
            continue

        try:
            # 進行推斷
            clean_clothing_images = model.infer(image)
            
            # 保存或顯示提取出的乾淨服裝區域
            base_filename = os.path.basename(image_path)
            filename, ext = os.path.splitext(base_filename)

            upper_wear_classes = [
                "long_sleeved_shirt",
                "long_sleeved_outwear",
                "short_sleeved_shirt",
                "short_sleeved_outwear",
                "long_sleeved_dress",
                "vest",
                "vest_dress",
                "dress"
            ]

            lower_wear_classes = [
                "shorts",
                "skirt",
                "trousers"
            ]

            for item in clean_clothing_images:
                clean_clothing_region = item["clean_clothing_region"]
                class_name = item["classes"]

                if class_name in upper_wear_classes:
                    base_output_path = os.path.join(output_folder, f"12_{filename}_E")
                elif class_name in lower_wear_classes:
                    base_output_path = os.path.join(output_folder, f"12_{filename}_Q")
                else:
                    base_output_path = os.path.join(output_folder, f"{filename}_{class_name}")

                output_path = get_output_path(base_output_path, "", ext)
                clean_clothing_region.save(output_path)
                print(f"Saved: {output_path}")

                # 計算類別數量
                if class_name in class_count:
                    class_count[class_name] += 1
                else:
                    class_count[class_name] = 1
        
        except Exception as e:
            print(f"Error processing image {image_path}: {str(e)}")
    
    # 輸出每個類別的數量
    print("Class counts:")
    for class_name, count in class_count.items():
        print(f"{class_name}: {count}")

if __name__ == "__main__":
    input_folder = "occasion:wedding_guest"
    output_folder = "cut_occasion:wedding_guest"

    process_folder(input_folder, output_folder)
