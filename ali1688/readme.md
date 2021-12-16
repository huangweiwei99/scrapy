https://s.1688.com/

### 先获取链接
字符串链接

```javascript 
let url = ''
clear();
items = document.querySelectorAll('#sm-offer-list > div > div > div.mojar-element-title > a')
Array.from(items).forEach(t => {
    // console.log(t.href)
    url = url + t.href.split('?')[0] + '\n'
})
console.log(url)
```

数组链接
```javascript
let url = []
clear();
items = document.querySelectorAll('div[class="zg-grid-general-faceout"] > div')
Array.from(items).forEach(t => {
    // console.log(t.href)
    url.push(t.querySelector('a').href.split('/ref=')[0] + '?th=1')
    // url = url + t.querySelector('a').href.split('/ref=')[0] + '\n'
})
console.log(JSON.stringify(url))
```

