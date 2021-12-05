let url = ''
clear();
items = document.querySelectorAll('.img-container > .mojar-element-image >a')
Array.from(items).forEach(t => {
    // console.log(t.href)
     url = url + t.href + '\n'
})
console.log(url)