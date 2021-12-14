// #app > div > div.iamgesaerch-offer-list-wrapper > div > div > div > div > div.bc-ife-gallery-item-title.bc-ife-gallery-item-title-line2 > a
let url = []
clear();
items = document.querySelectorAll("#app > div > div.iamgesaerch-offer-list-wrapper > div > div > div > div > div.bc-ife-gallery-item-title.bc-ife-gallery-item-title-line2 > a\n")
Array.from(items).forEach(t => {
    // console.log(t.href)
    url.push(t.href)
    // url = url + t.querySelector('a').href.split('/ref=')[0] + '\n'
})
console.log(JSON.stringify(url))