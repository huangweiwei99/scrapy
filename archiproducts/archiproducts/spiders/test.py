import scrapy
from scrapy import Request


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['archiproducts.com']

    # start_urls = ['http://archiproducts.com/']

    def start_requests(self):
        requesta = Request.from_curl("""curl 'https://www.archiproducts.com/api/products/productpopcontact?culture=zh' \
  -H 'authority: www.archiproducts.com' \
  -H 'sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"' \
  -H 'accept: */*' \
  -H 'content-type: application/json; charset=UTF-8' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'origin: https://www.archiproducts.com' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: empty' \
  -H 'referer: https://www.archiproducts.com/zh/%E4%BA%A7%E5%93%81/b-b-italia/%E6%89%B6%E6%89%8B%E6%A4%85-harbor-laidback-%E6%89%B6%E6%89%8B%E6%A4%85_549371' \
  -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6' \
  -H 'cookie: .AspNetCore.Antiforgery.xgdWZ61DnJU=CfDJ8LjLycKeI7tDvYZLTeTDfoa_fNE46UUeo22Nl7ktCPmW2mCW224SYJUdyikmNvnNyKQfot-dW6ZBqeLBPSzmmdmCVqjls55kRD7EJoeo926-22_bhT0nrbrFM8OUvF_1uWnub5hzO2PTm7xaDWm-Va0; _gcl_au=1.1.965289613.1638401228; awin_source=aw; __asc=777333f717d7852be9c03db9fc7; __auc=777333f717d7852be9c03db9fc7; _ga=GA1.2.2081636052.1638401229; _gid=GA1.2.1806957573.1638401229; _fbp=fb.1.1638401228956.966047502; _pin_unauth=dWlkPVpHSTFZVEF3T0RJdE1HVXpaaTAwWlRVekxXRTNNakV0TlRGbU5qazFaalE1TURWag; cf_chl_2=3360bc321f18ec8; cf_chl_prog=x9; cf_clearance=9abl5t4UUpjayJjXyYBKxplJkP9i6X5DMtQSOW1S6uE-1638401242-0-150; __cf_bm=t5dr8byQPd7Tfdg1gSCIsvvBPcG.Rh7R3ikP00s.JFk-1638401244-0-AUZGds7R04JRwZxPYmpm2JOHv4QqCK8ZUp4nhNxxO2PoIubdVLZnOKT6i8TkVzIFK6Xe1M7L46bBJMlfpYqR6v0GcG39gAZe64jr4V950h1YGxW3OHTsdXtZu/DEUEm3Km+QEA5iBAHnnCpuDUmuCQgFmuXDtSA9jL6cr+MN03tZ; .AspNetCore.IdentityCore=CfDJ8LjLycKeI7tDvYZLTeTDfoY3ygfpvX0ao6_DgNk3hQFvOulawnMChN6Yv9wtqdiSmEga1VO0iBPwoEfvPpfyPsh5kxliTdHuIVUSzC33pKfZs4qdfNrrRfsEAt4kPYWrotBVAe-e4SjRzadXNo7dc_sug4ml3d5w10y74fMWulHZ3oiK3fh9xVzNelLbcXsQXvQGY4rJLKBmbJcEFUOWgkoqR9wv9I4BtR2XfX19Gir6XZOZJVIuIplDk2L8lX23JTCv36prh1av18jCpTk2wmqTFhDM5eXgAGj6dIrrM8Zjt-Y8uSTkWnjF9OLxN8Cs_6vJ3WCEL9O5Fg4UErQZxkZaWuPluaJ_BcOyM7um-GubaayOKxVV8h0JB92Nj6ZEJO9L7l5gVDbzOlzBqU7fE8je74Nbe9OWK-SDk0bWhK8sQa-ntXQMzYz4gBtH2wVtmq4rGcgSVr79arDNjSoLZghoIe0QhmBoA_m1Ns78iGA4ew-uaM9uJbUityqEyuZQEp_6FD-c7xmXktcO2gPwU_wWPIrpZBPdTgLlk4xj77-1sa-gw0oA_sTjcHl-kOeiqLhARbcTsvxzOA6bSNPjqEp9s2bAl7gurf2WtCeRuN6E00BLoBygrVSv-x3eYGMqOqIuHszImTOZffpIWAHnnjVZolq2Bpf7mtqfXhjvOk0PTFFyWQi-g8DFDxTOG7Z-Xa44iIXjow0EvRDhLTkOzP3NZyfVoNth544pAEZWWv-zFNtVG64en_YcSGiEC508FB1iQ9qrh15y7-wKjNOXQ8ivSxTaM64Rr1oThJI9YqHsokBKlVHAdiAT63CfSCCwaHvAfeAojBD3B6Ehq06iNvdJ_JjUgW4hwKKgn81I4C-g; __zlcmid=17KkWUpdxz6ozU9' \
  --data-raw '{"userData":{"companyName":"","email":"dasd@ssss.com","geoInfo":{"geonameId":5128581,"regionCode":"","shortCountry":"US","shortProvince":"","address":"","city":"纽约","number":null},"jobId":107,"lastName":"kolo","name":"Linkoa","phoneNumber":null},"elementData":{"culture":"zh","elementId":549371,"eventObjectId":3022727,"eventType":2,"portalSource":4,"requestPageUrl":"https://www.archiproducts.com/zh/%E4%BA%A7%E5%93%81/b-b-italia/%E6%89%B6%E6%89%8B%E6%A4%85-harbor-laidback-%E6%89%B6%E6%89%8B%E6%A4%85_549371","canvas":0},"manufacturerId":76907,"utm":null}' \
  --compressed""")

        requesta.callback = self.parse

        yield requesta

    # for i in self.start_urls:
    #     yield scrapy.Request(url=i, meta={
    #         'dont_redirect': True,  # 这个可以
    #         'handle_httpstatus_list': [301, 302]  # 这个不行
    #     }, callback=self.parse)

    def parse(self, response):
        print(response.text)
