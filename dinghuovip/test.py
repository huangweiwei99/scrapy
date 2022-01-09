import html
import json
import re
from html.parser import HTMLParser

with open("./bsjj.json", 'r') as load_f:
    load_dict = json.load(load_f)
    for i in load_dict:
        print(i['Name'])
        print(i['ModelNum'])
        print(re.findall(r'src="(.*?)"', html.unescape(i['Description'])))
        print(i['ProductImgList'])
