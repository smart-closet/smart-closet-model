
# 衣服辯識
## identify_cloth_feature(img_path)
### 用途:
輸入圖片(單件服飾)位置，輸出辯識到的服裝資訊
### 函式的輸入與輸出
輸入:

`identify_cloth_feature(圖片位置)`

輸出:

一個 dictionary， 分為材質花紋風格及種類。

{'材質': ['cotton'], '花紋': ['graphic', 'print'], '風格': [], '種類': ['t-shirt']}
### Note
1. 覺得目前可以只篩材質跟種類就好，花紋如果跟Rule_base 得出來的結果不一樣沒關係
2. 目前 Gemnize 給他跑兩次取交集(多3秒)，不過還是有機率兩次都辯識到下衣的部分，所以看覺得要不要刪(也有可能我丟的照片是直接網路抓，DF2可能比較會切?)
***
# Rule_base

## getWeatherData ( city , place , current_Time )
### 用途:
抓取現在天氣資訊 (需要輸入所在地!, 時間是 optional 如果想查明天的也可以，default 是現在)

## 函式的輸入與輸出
輸入:

getWeatherData(城市名稱 , 鄉or鎮or市or區 , 時間 [可略,default 為現在時間] )

輸出:

{'體感溫度','溫度', '舒適度指數', '天氣預報綜合描述','6小時降雨機率'}

## Example
執行:

```getWeatherData('臺北市','大安區')```

得到結果:

{'體感溫度': '42', '溫度': '36', '舒適度指數': '31', '天氣預報綜合描述': '午後短暫雷陣雨。降雨機率 90%。溫度攝氏36度。悶熱。東北風 平均風速1-2級(每秒2公尺)。相對濕度59%。', '6小時降雨機率': '90'}

### Note

1. 需要定位當前地址才能夠有 city 及 place 的參數傳入 
2. 資料的時間範圍是該地，2天內的天氣資訊，每3個小時更新一次，取最近的下個預測
3. 好像andriod app 有手機定位功能，這裡就打算丟給後面做 app 時寫定位
   https://medium.com/@ntougpslab/7-%E5%AE%9A%E4%BD%8D%E5%8F%8Agoogle-map-2b9565c52877

## 參考的網站
### 中央氣象署開放資料平臺 api 文件
https://opendata.cwa.gov.tw/dist/opendata-swagger.html#/
### 全台鄉鎮市對照表
https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf
***
## weather_rule_Base(input_data, personal_temp=0)
### 用途:
輸入天氣資訊，輸出該天氣資訊下適合的衣服標籤

### 函式的輸入與輸出
輸入:

getWeatherData(天氣資訊,個人體感溫度)

輸出:

{'體感溫度','材質', '種類', '外套','備註'}

Example:

* 極端熱
  
{'體感溫度': [39], '材質': [['cotton', 'linen', 'linen-blend', 'satin', 'denim']], '種類': [['shirt', 'knit-top', 't-shirt', 'tank-top', 'dress', 'skirt', 'suit-pants', 'polo-shirt', 'yoga-pants', 'shorts', 'pants', 'cotton-pants', 'sweatpants', 'long-skirt', 'jeans', 'yoga-pants', 'jumpsuit', 'overalls', 'leggings']], '外套': [], '備註': []}

* 溫度介於 14~25 (ex 22)


{'體感溫度': [24, 22, 20], '材質': [['cotton', 'linen', 'linen-blend', 'satin', 'denim'], ['cotton', 'linen', 'linen-blend', 'satin', 'denim'], ['velvet', 'cotton', 'woven', 'crochet', 'faux-fur', 'faux-leather']], '種類': [['tank-top', 'dress', 'skirt', 'shorts', 't-shirt', 'shirt', 'polo-shirt', 'tank-top', 'suit-pants', 'sheer', 'pants', 'cotton-pants', 'sweatpants', 'long-skirt', 'jeans', 'jumpsuit', 'overalls', 'leggings'], ['dress', 'pants', 'shorts', 'suit-pants', 'yoga-pants', 'overalls', 'pants', 'cotton-pants', 'sweatpants', 'long-skirt', 'jeans', 'jumpsuit', 'overalls', 'leggings'], ['button-up-shirt', 'flannel-shirt', 'hoodie', 'turtleneck', 'pants', 'cotton-pants', 'sweatpants', 'long-skirt', 'jeans', 'jumpsuit', 'overalls', 'leggings']], '外套': [['vest', 'cotton-vest'], ['vest', 'cotton-vest'], ['sweater-vest', 'jacket', 'suit-jacket', 'denim-jacket']], '備註': []}

* 偏冷 13 度下 (極冷5度下):

(ex: 13)

{'體感溫度': [13], '材質': [['velvet', 'cotton', 'woven', 'crochet', 'faux-fur', 'faux-leather']], '種類': [['wool-pants', 'turtleneck', 'windproof-pants', 'hoodie', 'college-sweatshirt', 'sweater', 'pants', 'cotton-pants', 'sweatpants', 'long-skirt', 'jeans', 'jumpsuit', 'overalls', 'leggings', 'sweatpants']], '外套': [['insulated-vest', 'leather-jacket', 'coat', 'trench-coat', 'cotton-coat', 'padded-jacket', 'down-jacket']], '備註': []}

(ex: 5)

{'體感溫度': [5], '材質': [['velvet', 'cotton', 'woven', 'crochet', 'faux-fur', 'faux-leather']], '種類': [['wool-pants', 'turtleneck', 'windproof-pants', 'hoodie', 'college-sweatshirt', 'sweater', 'pants', 'cotton-pants', 'sweatpants', 'long-skirt', 'jeans', 'jumpsuit', 'overalls', 'leggings', 'sweatpants']], '外套': [['padded-jacket', 'down-jacket', 'ski-jacket', 'winter-sportswear']], '備註': ['thermal-underwear']}
  

### Note
1. 溫度如果介於14~25會提供3個溫度的選項，其他天氣歸類於極端氣候只會產生一個溫度
2. Personal temp 是供使用者調整個人溫度，如果想要加暖1度:personal temp 傳 1, 想要變冷1度: personal temp -1
3. 備註是指有霸王寒流才會將發熱衣寫再備註
4. 覺得外套的部分可以再配好的衣服後，根據顏色選互補搭配
***

## occation_filter(user_occation)
### 用途:
輸入使用者場合，輸出該場合適合的服飾及是否室內活動。

### 函式的輸入與輸出
輸入:

`occation_filter(使用者場合)`

輸出:

{'場合':[],'材質':[],'種類':[],'戶外與否':[]}

Example:

'場合': 'Daily_Work', '材質': ['denim', 'cotton', 'leather', 'stripped', 'print'], '種類': ['dress-shirt', 'jeans', 't-shirt', 'sweater', 'pants', 'long-skirt', 'cotton-pants'], '戶外與否': True}

### Note
1. 場合限定為10種分別有 Dating、Daily_Work、Travel、Sports、Conference、Prom、Shopping、Party、School、Wedding_Guest
2. 覺得 Conference 和 Daily_work 可以合併成 Formal
***
## Rule_Base_filter(city,place,consider_weather=True, user_occation='None',personal_temp=0):
### 用途:

輸入使用者位置及context，輸出符合所有條件的衣服標註

### 函式的輸入與輸出
輸入:

`Rule_Base_filter(城市,鄉鎮市區,是否考量天氣, 是否考量場合,個人化溫度調整)`

輸出:

1. 只考量場合(或是選擇天氣+室內的場合)

{'場合':[],'材質':[],'種類':[],'戶外與否':[]}

Example:

`print(Rule_Base_filter('臺北市', '大安區',consider_weather=False, user_occation='Daily_Work'))`

{'場合': 'Daily_Work', '材質': ['denim', 'cotton', 'leather', 'stripped', 'print'], '種類': ['dress-shirt', 'jeans', 't-shirt', 'sweater', 'pants', 'long-skirt', 'cotton-pants'], '戶外與否': True}

2. 只考量天氣

{'體感溫度':[],'材質':[],'種類':[],'外套:[]','備註':[]}

Example:

`print(Rule_Base_filter('臺北市', '大安區',consider_weather=True))`       

{'體感溫度': [35], '材質': [['cotton', 'linen', 'linen-blend', 'satin', 'denim']], '種類': [['suit-pants', 'shirt', 'skirt', 'tank-top', 'knit-top', 't-shirt', 'dress', 'yoga-pants', 'sheer', 'shorts', 'polo-shirt', 'pants', 'cotton-pants', 'sweatpants', 'long-skirt', 'jeans', 'jumpsuit', 'overalls', 'leggings']], '外套': [], '備註': []}


3. 考量天氣與場合

{'體感溫度':[],'材質':[],'種類':[],'外套:[]','備註':[]}

Example:

`print(Rule_Base_filter('臺北市', '大安區',consider_weather=True,user_occation='Sports'))`       

{'體感溫度': [35], '材質': [['cotton']], '種類': [['sweatpants', 'shorts', 't-shirt', 'pants', 'yoga-pants']], '外套': [], '備註': []}

