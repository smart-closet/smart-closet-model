# good
### 0. 取出好的 outfits
要同時有上衣、下衣，才能計入。

不重要的 output:<br/>`good_outfits_america.csv`（1013 筆資料）、<br/>`good_outfits_japan.csv` （849 筆資料）、<br/>`good_outfits_korea.csv`（698 筆資料）。

格式與下述的 `good_outfits.csv` 相同。


### 1. 每個 style 各取出 698 個 outfits
output: `good_outfits.csv`

格式：
``` csv=
index,img_path,img_pathE,img_pathQ
0_1,../new_data/style:america/1.jpg,../new_data/cut_style:america/0_1_E_.jpg,../new_data/cut_style:america/0_1_Q_.jpg
```

### 2. end

---

# bad
### 0. 有哪些 E, Q
讀入 `good_outfits.csv`，生成可以配對的 E, Q。

### 1. random
三種風格各 698 張<br />
歐美 349 張上衣 + 日系 349 張下衣<br />
歐美 349 張上衣 + 韓系 349 張下衣<br />
以此類推

### 2. check
確保每張照片都有分配到

### 3. output csv file
output: `bad_outfits.csv`

格式：
```csv=
idxE, idxQ, img_pathE, img_pathQ
0_579_E_,1_997_Q_,../new_data/cut_style:america/0_579_E_.jpg,../new_data/cut_style:japan/1_997_Q_.jpg
```

### 4. end