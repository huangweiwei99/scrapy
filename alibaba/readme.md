### 产品详情页面
获取 json 格式的详情
```python
detail_data_str = ''
    for i in response.xpath('//script').extract():
        if len(re.findall(r'window.detailData', i)) > 0:
            for j in i.split('\n'):
                if len(re.findall(r'window.detailData', j)) > 0:
                    detail_data_str = j.split('window.detailData = ')[-1]
            break
    detail_data = json.loads(detail_data_str)
```
### 一年内的产品交易情况
https://taopinpin.en.alibaba.com/event/app/productExportOrderQuery/transactionOverview.htm?detailId=1600145084062&languageType=en
```json
{"code":200,"success":true,"data":{"dateRange":"2020\/12\/01-2021\/11\/28","totalTransactions":7,"totalQuantities":9,"totalBuyers":7,"chartData":[{"month":"2020-12","transactions":4},{"month":"2021-01","transactions":0},{"month":"2021-02","transactions":0},{"month":"2021-03","transactions":2},{"month":"2021-04","transactions":0},{"month":"2021-05","transactions":0},{"month":"2021-06","transactions":1},{"month":"2021-07","transactions":0},{"month":"2021-08","transactions":0},{"month":"2021-09","transactions":0},{"month":"2021-10","transactions":0},{"month":"2021-11","transactions":0}]},"message":""}
```
###  交易国家
https://taopinpin.en.alibaba.com/event/app/productExportOrderQuery/transactionCountries.htm?detailId=1600145084062
```json
{"code":200,"success":true,"message":"","data":[{"buyerCountry":"UZ","countryFullName":"Uzbekistan"},{"buyerCountry":"CA","countryFullName":"Canada"},{"buyerCountry":"US","countryFullName":"United States"}]}
```

### 产品对比
https://www.alibaba.com/detail/compareProducts.html?ids=1600388112860,1600178968560

### 搜索结果API

```
https://open-s.alibaba.com/openservice/galleryProductOfferResultViewService?appName=magellan&appKey=a5m1ismomeptugvfmkkjnwwqnwyrhpb1&staticParam=&SearchText=living_room_sofa&IndexArea=product_en&page=1&waterfallCtrPageId=453bc45bd4884cd5a2ec421934c12dab&waterfallReqCount=1&asyncLoadIndex=1&asyncLoad=true&callback=__jp5

https://open-s.alibaba.com/openservice/galleryProductOfferResultViewService?appName=magellan&appKey=a5m1ismomeptugvfmkkjnwwqnwyrhpb1&staticParam=&SearchText=living_room_sofa&IndexArea=product_en&page=1&waterfallCtrPageId=453bc45bd4884cd5a2ec421934c12dab&waterfallReqCount=1&asyncLoadIndex=2&asyncLoad=true&callback=__jp5
```

```
https://open-s.alibaba.com/openservice/galleryProductOfferResultViewService?appName=magellan&appKey=a5m1ismomeptugvfmkkjnwwqnwyrhpb1&staticParam=&SearchText=living_room_sofa&IndexArea=product_en&page=2&waterfallCtrPageId=b760dabb573e46cdbec1dbbf6deefc74&waterfallReqCount=1&asyncLoadIndex=1&asyncLoad=true&callback=__jp3


https://open-s.alibaba.com/openservice/galleryProductOfferResultViewService?appName=magellan&appKey=a5m1ismomeptugvfmkkjnwwqnwyrhpb1&staticParam=&SearchText=living_room_sofa&IndexArea=product_en&page=2&waterfallCtrPageId=b760dabb573e46cdbec1dbbf6deefc74&waterfallReqCount=1&asyncLoadIndex=2&asyncLoad=true&callback=__jp3

page=101 0-0

asyncLoadIndex=1|2

SearchText=living_room_sofa



```
#### 获取搜索产品链接
```javascript
clear()
arr=[]
Array.from(document.querySelectorAll("#app > div > div.iamgesaerch-offer-list-wrapper > div > div > div > div > div.bc-ife-gallery-item-title.bc-ife-gallery-item-title-line2 > a")).forEach(function(item) {
 
    href=item.href
    arr.push(href)

 });
//  console.log(arr)
 console.log(JSON.stringify(arr))
```

---
> https://www.osgeo.cn/scrapy/topics/developer-tools.html#the-network-tool
> 
> https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/feed-exports.html#topics-feed-format-jsonlines