# 顏色辯識
1. 辯識衣服所呈現顏色，並將相對比例以 pie chart 呈現，按規則選主色
2. 與 Fashion semantic space 定義的顏色算相似程度並選出代表色


## 辯識衣服主色 (k-means)
衣服會因為皺褶或光線因素而存在多種顏色，
又深色的衣服吸光，在光線下不容易變色，
而淺的衣服則容易存在陰影而出現多種不同的顏色，
因此定義衣服的主色為 -> 比例大於 15% (這個%數可以調整)之中，亮度最大的那個顏色 + 若有任何顏色超過 45% 則定義為主色 

### Example
如果直接選用比例最大的則會變是成棕色(45%)，調整後會選 color-3(橘色)
<div style="display: flex; justify-content: space-between;">
  <img src="https://github.com/smart-closet/smart-closet-model/blob/main/phase1/Color_identification/orange.png" alt="orange" width="200" style="margin-right: 10px;"/>
  <img src="https://github.com/user-attachments/assets/b7c28d7c-d927-4155-910c-fdb640184727" alt="image" width="400"/>
</div>
在下面這張則會選 color-2
<div style="display: flex; justify-content: space-between;">
  <img src="https://github.com/smart-closet/smart-closet-model/blob/main/phase1/Color_identification/jeans.png" alt="orange" width="200" style="margin-right: 10px;"/>
  <img src="https://github.com/user-attachments/assets/4540e7bc-9862-4f1a-8610-00de5d2f9db0" alt="image" width="400"/>
</div>

## 與 Fahsion Semantic sapce 串聯並選出代表色
### Fashion Semantic Space
<img src="https://github.com/user-attachments/assets/74a86b9b-354e-448c-8e6f-5e55852ffedf" alt="orange" width="800"/>

### 手動汲取顏色將照片轉成 Hex 代碼

```
colors_dict = {
    "ROMANTIC": {
        "sweet & dreamy":["#f7b4ad","#fce5c8","#cbbdd8"],
        "romantic":["#cbbcd9","#ffffff","#c7e8ec"],
        "pure & genuine":["#e7dae4","#ffffff","#d7e2e9"]
    },
    "NATURAL": {
        "domestic":["#fac6a3","#fef3c3","#aeba9d"],
        "tranquil":["#aeba9d","#d2c3a2","#e8ebb7"],
        "delicate":["#e6dae4","#d7c3c5","#afc2ca"],
        "feminine":["#d5c3c5","#fadcd1","#f5bbc5"],
        "elegant":["#a78eb9","#d2b3ae","#c5c6ca"]
    },
    "ELEGANT": {
        "graceful":["#cc95a2","#927d84","#7a6487"],
        "artistic & tasteful":["#947f62","#c4bdc4","#868b6c"]    },
    "CLEAR": {
        "clean":["#d5e2e9","#ffffff","#d6eae5"],
        "refreshing":["#94d4e1","#ffffff","#b4cdd6"]
    },
    "COOL CASUAL": {
        "young":["#fdeb92","#93cc9e","#7eafdc"],
        "youthful":["#73c594","#ffffff","#0066b0"],
        "exhilarating":["#55c4cf","#fefffe","#124e8d"]
    },
    "MODERN": {
        "speedy":["#221816","#feffff","#0265ae"],
        "modern":["#98999e","#221816","#018491"],
        "rational":["#222d4d","#fffffe","#221816"],
        "exact":["#134d8c","#86909c","#2a2422"]
    },
    "CHIC": {
        "polished":["#a3bbc4","#dae5e7","#98c2c8"],
        "chic":["#77767b","#b1b2b6","#c4bdc4"],
        "cerebral":["#436a8c","#e2e1e1","#49a5ae"]
    },
    "STYLISH": {
        "earnest":["#211816","#c6c6ca","#1b518c"],
        "dapper": ["#440f18","#937f61","#043440"]
    },
    "CASUAL": {
        "lighthearted": ["#f7c88e","#fdf3c8","#bbd660"],
        "enjoyable":["#f38472","#feea93","#74c494"],
        "perky":["#fab16b","#36baa4","#ffe760"],
        "casual":["#d92131","#fefffe","#0066af"]
    },
    "PRETTY": {
        "naive":["#f7b4ab","#fdf4c5","#fbc6a4"],
        "childlike":["#f7b4ab","#fdf3c4","#90d5e1"]
    },
    "DYNAMIC": {
        "active":["#221816","#da2130","#0066b0"],
        "bold":["#da2131","#221916","#fce830"],
        "energetic":["#231815","#f69121","#862c28"]
    },
    "GORGEOUS": {
        "captivating":["#c1547e","#221816","#7d5997"],
        "luxurious":["#c7af2f","#98272e","#231815"],
        "extravagant":["#423366","#928039","#812754"]
    },
    "CLASSIC": {
        "tasteful":["#a16158","#460e19","#987f7e"],
        "traditional":["#413366","#a16031","#4e6838"]
    },
    "CLASSIC & STYLISH": {
        "genuine":["#4d331c","#a0877d","#460e19"],
        "serious":["#221816","#71592e","#460e19"]
    },
    "FORMAL": {
        "sacred":["#362b49","#b1b2b5","#221816"]
    },
    "WILD": {
        "robust":["#4e3f1f","#99272e","#4e6e74"],
        "wild": ["#98282d","#221815","#085e39"]
    }
}
```

### 用 RGB 比例 + HSV 進行相似度處理
(這邊還是要在研究一下)
一個解決的方法是存種類不存顏色，就可能給用戶看辯識出來的顏色，但後端存的是 "chic"

<div style="display: flex; justify-content: space-between;">
  <img src="https://github.com/smart-closet/smart-closet-model/blob/main/phase1/Color_identification/ppp.png" alt="orange" width="200" style="margin-right: 10px;"/>
  <img src="https://github.com/user-attachments/assets/96ee41f0-7c50-4ca8-9dfc-3463e61972e1" alt="image" width="200"/>
  <img src="https://github.com/user-attachments/assets/17c465df-2504-4d5e-b640-c5a0f8f73a02" alt="image" width="200"/>
  <img src="https://github.com/user-attachments/assets/69c5b55f-89c7-4c12-9974-637a699feb35" alt="image" width="200"/>
</div>








