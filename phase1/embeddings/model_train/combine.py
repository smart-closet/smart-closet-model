import pandas as pd

# 读取两个 CSV 文件
df1 = pd.read_csv('phase1/embeddings/model_train/good_embedding_CNN.csv')
df2 = pd.read_csv('phase1/embeddings/model_train/ugly_embedding_CNN.csv')

# 合并数据
combined_df = pd.concat([df1, df2], ignore_index=True)

# 打乱数据顺序
shuffled_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)

# 输出打乱后的 DataFrame 到新的 CSV 文件
shuffled_df.to_csv('mix_embedding_cnn.csv', index=False)
