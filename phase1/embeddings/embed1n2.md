### 0. model

取出 `im-project-main/models` 下的 DeepFashion1

### 1. img2vec
(function)<br />
input: imgE_path, imgQ_path<br />
output: probability embedding, multi-hot embedding

### 2. good data

**之後可能要改 path、改格式**<br />
input: `good_outfits.csv`<br />
output: `good_embedding_probEQ.csv`, `good_embedding_predEQ.csv`

假想 input 好的 outfits 的格式：
``` csv=
index, img_path, img_pathE, img_pathQ
```
假想 output 好的 embedding 的格式：
``` csv=
index, img_path, embedEQ, label(1), embedE, embedQ
```

### 3. bad data

**之後可能要改 path、改格式**<br />
input: `bad_outfits.csv`<br />
output: `bad_embedding_probEQ.csv`, `bad_embedding_predEQ.csv`

假想 input 糟糕的 outfits 的格式：
``` csv=
idxE, idxQ, img_pathE, img_pathQ
```
假想 output 糟糕的 embedding 的格式：
``` csv=
idxE, idxQ, img_pathE, img_pathQ, embedEQ, label(0), embedE, embedQ
```

### 4. end