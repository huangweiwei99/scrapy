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

