import pickle
import pandas as pd

# 讀取 .pkl 檔案
with open('phase1/embeddings/model_train/good_embedding.pkl', 'rb') as file:
    data = pickle.load(file)

# 將資料轉換為 DataFrame
df = pd.DataFrame(data)

# 儲存為 .csv 檔案
df.to_csv('phase1/embeddings/model_train/good_embedding_CNN.csv', index=False)
