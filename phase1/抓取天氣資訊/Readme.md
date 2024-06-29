# getWeatherData(city,place,current_Time)


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

## Note

1. 需要定位當前地址才能夠有 city 及 place 的參數傳入 (目前設定式寫在函式外面或是要在裡面也可以)
2. 資料的時間範圍是該地，2天內的天氣資訊，每3個小時更新一次，取最近的下個預測

## 參考的網站
### 中央氣象署開放資料平臺 api 文件
https://opendata.cwa.gov.tw/dist/opendata-swagger.html#/
### 全台鄉鎮市對照表
https://opendata.cwa.gov.tw/opendatadoc/Opendata_City.pdf


