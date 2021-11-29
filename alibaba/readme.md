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

