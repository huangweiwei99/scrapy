import json
import re
from copy import deepcopy

import scrapy

from ..items import DetailItem


class MoreDetailSpider(scrapy.Spider):
    name = 'more_detail'
    allowed_domains = ['alibaba.com']
    start_urls = [
        "https://www.alibaba.com/product-detail/SF-150-Stanley-Leather-Sofa-India_60427960980.html?spm=a2700.picsearch.offer-list.2.1c955f933CCsgW",
        "https://www.alibaba.com/product-detail/Hotel-lobby-furniture-luxury-italian-leather_60781407870.html?spm=a2700.picsearch.offer-list.6.1c955f933CCsgW",
        "https://www.alibaba.com/product-detail/Nordic-Modern-Luxury-Living-Room-Sofa_1600234732860.html?spm=a2700.picsearch.offer-list.10.1c955f933CCsgW",
        "https://www.alibaba.com/product-detail/Genuine-leather-living-room-velvet-sofa_1600360381592.html?spm=a2700.picsearch.offer-list.14.1c955f933CCsgW",
        "https://www.alibaba.com/product-detail/Hotel-1-2-3-Seater-Sofa_1600172158325.html?spm=a2700.picsearch.offer-list.18.1c955f933CCsgW",
        "https://www.alibaba.com/product-detail/Nordic-leather-sofa-American-industrial-style_1600316774377.html?spm=a2700.picsearch.offer-list.22.1c955f933CCsgW",
        "https://www.alibaba.com/product-detail/Product-Test_10000003601421.html?spm=a2700.picsearch.offer-list.26.1c955f933CCsgW",
        "https://www.alibaba.com/product-detail/AMERICAN-SOFA-Modern-style-couch-set_1600374025036.html?spm=a2700.picsearch.offer-list.30.1c955f933CCsgW",
        "https://www.alibaba.com/product-detail/Modern-simple-design-office-sofa-set_62049535914.html?spm=a2700.picsearch.offer-list.34.1c955f933CCsgW",
        "https://www.alibaba.com/product-detail/Tan-Faux-Leather-3-Seater-Tuxedo_1600369192912.html?spm=a2700.picsearch.offer-list.38.1c955f933CCsgW",
        "https://www.alibaba.com/product-detail/manager-room-office-sofa-for-customer_62515935091.html?spm=a2700.picsearch.offer-list.42.1c955f933CCsgW",
        "https://www.alibaba.com/product-detail/Nordic-light-luxury-small-apartment-sofa_1600320058793.html?spm=a2700.picsearch.offer-list.46.1c955f933CCsgW",
        "https://www.alibaba.com/product-detail/Modern-American-style-luxury-design-reclining_60799282087.html?spm=a2700.picsearch.offer-list.50.1c955f933CCsgW",
        "https://www.alibaba.com/product-detail/luxury-sectional-modern-leather-sofa-living_1600371520413.html?spm=a2700.picsearch.offer-list.54.1c955f933CCsgW",
        "https://www.alibaba.com/product-detail/Three-Seater-Antique-European-Genuine-Leather_62033978589.html?spm=a2700.picsearch.offer-list.58.1c955f933CCsgW",
        "https://www.alibaba.com/product-detail/Three-Seater-Antique-European-Genuine-Leather_62062437998.html?spm=a2700.picsearch.offer-list.62.1c955f933CCsgW",
        "https://www.alibaba.com/product-detail/Northern-Europe-Leisure-Single-Person-Sofa_1600236223782.html?spm=a2700.picsearch.offer-list.66.1c955f933CCsgW",
        "https://www.alibaba.com/product-detail/2-Seater-European-style-New-Classical_1600189607584.html?spm=a2700.picsearch.offer-list.70.1c955f933CCsgW",
        "https://www.alibaba.com/product-detail/Luxury-Wooden-Legs-Genuine-Leather-Mixed_62035646710.html?spm=a2700.picsearch.offer-list.74.1c955f933CCsgW",
        "https://www.alibaba.com/product-detail/Good-quality-modern-living-room-adjustable_1600294283859.html?spm=a2700.picsearch.offer-list.78.1c955f933CCsgW",
        "https://www.alibaba.com/product-detail/Home-furniture-recliner-couch-convertible-sofa_1600213240968.html",
        "https://www.alibaba.com/product-detail/Luxury-Furniture-Living-Room-Big-Sofa_1600355442652.html",
        "https://www.alibaba.com/product-detail/wholesale-double-seat-furniture-relaxing-brown_1600102821119.html",
        "https://www.alibaba.com/product-detail/Leather-sofa-combination-small-apartment-living_1600290368163.html",
        "https://www.alibaba.com/product-detail/S107-1-Simple-Design-Small-Office_60818577048.html",
        "https://www.alibaba.com/product-detail/Nordic-loft-modern-sectional-sofa-single_1600089378450.html",
        "https://www.alibaba.com/product-detail/Modern-Design-Adjustable-PU-Recliner-Sofa_1600283140635.html",
        "https://www.alibaba.com/product-detail/High-Density-Foam-Living-Room-Sofas_62525436125.html",
        "https://www.alibaba.com/product-detail/Italian-leather-corner-mid-century-modern_1600359044669.html",
        "https://www.alibaba.com/product-detail/Luxury-Top-Modern-Brown-Leather-Sofa_1600062610555.html",
        "https://www.alibaba.com/product-detail/Wholesale-Cheap-modern-living-room-adjustable_1600288712213.html",
        "https://www.alibaba.com/product-detail/SF-028-American-Italy-Genuine-Leather_60420968614.html",
        "https://www.alibaba.com/product-detail/Modern-Design-Brown-leather-upholstery-luxury_1600271282074.html",
        "https://www.alibaba.com/product-detail/Modern-design-grey-fabric-hotel-and_1600370476035.html",
        "https://www.alibaba.com/product-detail/Modern-1-1-3-seat-executive_60773322338.html",
        "https://www.alibaba.com/product-detail/High-Density-Foam-Living-Room-Sofas_1600404182182.html",
        "https://www.alibaba.com/product-detail/Italian-leather-corner-mid-century-modern_1600359105089.html",
        "https://www.alibaba.com/product-detail/Factory-Direct-Modern-Waiting-Area-3_1600293881587.html",
        "https://www.alibaba.com/product-detail/Fabric-corner-nordic-italian-fabric-modern_1600360484264.html",
        "https://www.alibaba.com/product-detail/Wild-Sensual-Nubuck-Leather-Sofa-Couch_1600388977774.html",
        "https://www.alibaba.com/product-detail/European-style-contemporary-design-solid-wood_1600374205252.html",
        "https://www.alibaba.com/product-detail/Genuine-leather-living-room-velvet-sofa_1600360229674.html",
        "https://www.alibaba.com/product-detail/Wholesale-the-latest-design-sofa-set_1600362711278.html",
        "https://www.alibaba.com/product-detail/SF-072-High-Quality-Genuine-Leather_60427659083.html",
        "https://www.alibaba.com/product-detail/Aesthetic-Hot-Sale-Modern-small-Space_1600303357976.html",
        "https://www.alibaba.com/product-detail/Recliner-Sofa-Living-Room-Furniture-Luxury_1600055330190.html",
        "https://www.alibaba.com/product-detail/2019-Public-Waiting-Area-Modern-Leather_60619763964.html",
        "https://www.alibaba.com/product-detail/Factory-Direct-Modern-Waiting-Area-3_1600274060529.html",
        "https://www.alibaba.com/product-detail/Modern-design-high-end-office-furniture_62233773695.html",
        "https://www.alibaba.com/product-detail/Hot-Sale-Antique-Leather-Lounge-Armchair_62317071174.html",
        "https://www.alibaba.com/product-detail/Luxury-Leather-Office-Sofa-High-End_1600160455423.html",
        "https://www.alibaba.com/product-detail/Italian-minimalist-sofa-technology-fabric-living_1600314910951.html",
        "https://www.alibaba.com/product-detail/2020-Popular-Office-Furniture-Modern-Design_62562710791.html",
        "https://www.alibaba.com/product-detail/2021-Luxury-Exquisite-Minimalist-Style-Teak_1600263805675.html",
        "https://www.alibaba.com/product-detail/Modern-bed-leather-design-sofas-sectionals_1600346806862.html",
        "https://www.alibaba.com/product-detail/Office-sofa-modern-minimalist-sofa-reception_1600361021281.html",
        "https://www.alibaba.com/product-detail/Designed-Client-meeting-sofa-for-the_1600332639381.html",
        "https://www.alibaba.com/product-detail/Upholstered-Modern-Simple-Designs-Leather-Lounge_1600336986265.html",
        "https://www.alibaba.com/product-detail/Customized-6-Seater-Sofa-Set-Living_1600287586001.html",
        "https://www.alibaba.com/product-detail/grey-independently-seat-cushion-pillows-commercial_1600361889179.html",
        "https://www.alibaba.com/product-detail/Modern-brown-leather-office-sofa-three_62226233097.html",
        "https://www.alibaba.com/product-detail/Modern-Office-Sofa-2-seater-living_1600242264965.html",
        "https://www.alibaba.com/product-detail/Custom-Made-Italian-Minimalism-Design-Furniture_1600323257301.html",
        "https://www.alibaba.com/product-detail/Hot-Selling-Modern-Good-Quality-3_60783710367.html",
        "https://www.alibaba.com/product-detail/Modern-brown-leahter-sectional-office-sofa_1600211366597.html",
        "https://www.alibaba.com/product-detail/3-seater-leather-upholstered-office-lounge_1600211361724.html",
        "https://www.alibaba.com/product-detail/Cowhide-office-sofa-combination-Nordic-minimalist_1600348544589.html",
        "https://www.alibaba.com/product-detail/Luxury-Top-Modern-Brown-Living-Room_1600273048860.html",
        "https://www.alibaba.com/product-detail/Foshan-Factory-business-area-waiting-room_62356190480.html",
        "https://www.alibaba.com/product-detail/Modern-design-new-model-genuine-leather_60704302770.html",
        "https://www.alibaba.com/product-detail/Simple-design-brown-leather-executive-office_1600057611744.html",
        "https://www.alibaba.com/product-detail/Genuine-Leather-Wooden-Sofa-Set-Living_1600273113516.html",
        "https://www.alibaba.com/product-detail/Restaurant-chair-with-metal-Leg-armchair_1600374233593.html",
        "https://www.alibaba.com/product-detail/Office-sofa-designs-for-office-room_1600066517863.html",
        "https://www.alibaba.com/product-detail/modern-living-room-sofa-leather-sectional_60772885656.html",
        "https://www.alibaba.com/product-detail/high-quality-banquet-home-furniture-velvet_1600384985080.html",
        "https://www.alibaba.com/product-detail/European-Style-Modern-Office-Brown-Leather_1600249913510.html",
        "https://www.alibaba.com/product-detail/hot-sell-modern-nordic-style-living_1600323497622.html",
        "https://www.alibaba.com/product-detail/cheap-grey-velvet-upholstered-home-furniture_62333374086.html",
        "https://www.alibaba.com/product-detail/New-American-stylemodern-living-room-furniture_1600141790708.html",
        "https://www.alibaba.com/product-detail/High-Quality-Factory-Sale-Best-Quality_1600231901496.html",
        "https://www.alibaba.com/product-detail/Hot-Sale-Home-Furniture-Living-Room_1600186322177.html",
        "https://www.alibaba.com/product-detail/The-new-lazy-super-large-single_1600169963478.html",
        "https://www.alibaba.com/product-detail/Leather-Love-Seat-High-Quality-Comfortable_62070969867.html",
        "https://www.alibaba.com/product-detail/Latest-Fashion-Flexible-Modular-Design-Fabric_1600302633436.html",
        "https://www.alibaba.com/product-detail/Fabric-corner-sofa-living-room-guangzhou_60486831718.html",
        "https://www.alibaba.com/product-detail/Sofa-BAS8316-Living-Room-Modern-Home_62013416093.html",
        "https://www.alibaba.com/product-detail/Factory-living-room-Furniture-Fabric-Chesterfield_1600208365313.html",
        "https://www.alibaba.com/product-detail/Customized-4-Seater-Sofa-Set-Living_1600287545498.html",
        "https://www.alibaba.com/product-detail/China-Popular-And-Practical-Luxury-Living_1600228811808.html",
        "https://www.alibaba.com/product-detail/Simple-design-leather-sofa-living-room_62341771802.html",
        "https://www.alibaba.com/product-detail/Office-furniture-modern-style-leather-sofa_1600370178275.html",
        "https://www.alibaba.com/product-detail/Luxury-Modern-Simple-Home-Furniture-Living_1600212022713.html",
        "https://www.alibaba.com/product-detail/PU-Leather-Office-Sofa-Set-Conference_1600343535799.html",
        "https://www.alibaba.com/product-detail/Manufacturers-latest-3-seater-modern-italian_62235077155.html",
        "https://www.alibaba.com/product-detail/Top-quality-modern-leather-sofa-for_62183596819.html",
        "https://www.alibaba.com/product-detail/Luxury-Furniture-corner-couch-one-two_1600252117627.html",
        "https://www.alibaba.com/product-detail/2-Seater-dual-sofa-European-style_1600193699580.html",
        "https://www.alibaba.com/product-detail/Foshan-Xuya-Cheap-office-sofa-set_1600364436466.html",
        "https://www.alibaba.com/product-detail/3-seat-80-7-L-33_1600361787566.html"]
    sku = 'S009'

    def parse(self, response):
        if response.status == 200:
            try:
                self.crawler.stats.inc_value('cnt')
                for i in response.xpath('//script').extract():
                    if len(re.findall(r'window.detailData', i)) > 0:
                        for j in i.split('\n'):
                            if len(re.findall(r'window.detailData', j)) > 0:
                                detail_data_str = j.split('window.detailData = ')[-1]
                                detail_data = json.loads(detail_data_str)
                                # print(json.dumps(detail_data))
                                item_id = detail_data['globalData']['product']['productId']
                                base_url = 'https://www.en.alibaba.com/event/app/productExportOrderQuery'
                                urls = [
                                    # 订单概览
                                    '{0}/transactionOverview.htm?detailId={1}'.format(base_url, item_id),
                                    # 出口国家
                                    '{0}/transactionCountries.htm?detailId={1}'.format(base_url, item_id),
                                    # 详细订单
                                    '{0}/transactionList.htm?&size=1000&detailId={1}'.format(base_url, item_id)
                                ]
                                self.crawler.stats.set_value('detail', [])
                                detail_data = detail_data['globalData']
                                detail_data.pop('i18n', '')
                                detail_data['sku'] = self.sku
                                yield from response.follow_all(urls=urls, callback=self.parse_transaction,
                                                               dont_filter=True,
                                                               meta={'detail': deepcopy(detail_data)})
                        break

            except Exception as e:
                print('----------------')
                print('解析详情页出错')
                print(response.request.url)
                print(e)
                print('----------------')
        else:
            print('网络错误')

    def parse_transaction(self, response):
        if response.status == 200:
            try:
                url = response.request.url
                item_id = url.split('=')[-1]
                meta_detail = response.meta['detail']
                if str(meta_detail['product']['productId']) == item_id:
                    # 设置初始数据
                    k_detail = self.crawler.stats.get_value('detail')
                    if 'transaction_overview' not in k_detail \
                            and 'transaction_countries' not in k_detail \
                            and 'transaction_list' not in k_detail:
                        # print('start')
                        self.crawler.stats.set_value('detail', meta_detail)

                    if len(re.findall(r'transactionOverview', url)) > 0:
                        # print('transactionOverview')
                        res_data = json.loads(response.text)
                        detail = self.crawler.stats.get_value('detail')
                        detail['transaction_overview'] = res_data['data'] if res_data['success'] else []
                        self.crawler.stats.set_value('detail', detail)
                        # print('-------------------------------------')

                    elif len(re.findall(r'transactionCountries', url)) > 0:
                        # print('transactionCountries')
                        res_data = json.loads(response.text)
                        detail = self.crawler.stats.get_value('detail')
                        detail['transaction_countries'] = res_data['data'] if res_data['success'] else []
                        self.crawler.stats.set_value('detail', detail)
                        # print('-------------------------------------')

                    elif len(re.findall(r'transactionList', url)) > 0:
                        # print('transactionList')
                        res_data = json.loads(response.text)
                        detail = self.crawler.stats.get_value('detail')
                        detail['transaction_list'] = res_data['data']['orders'] if res_data['success'] else []
                        self.crawler.stats.set_value('detail', detail)
                        # print('-------------------------------------')

                    # 三次查询后返回结果
                    k_detail = self.crawler.stats.get_value('detail')
                    if 'transaction_overview' in k_detail \
                            and 'transaction_countries' in k_detail \
                            and 'transaction_list' in k_detail:
                        detail = self.crawler.stats.get_value('detail')
                        yield DetailItem(
                            abtest=detail['abtest'],
                            buyer=detail['buyer'],
                            extend=detail['extend'],
                            product=detail['product'],
                            risk=detail['risk'],
                            seller=detail['seller'],
                            seo=detail['seo'],
                            trade=detail['trade'],
                            transaction_list=detail['transaction_list'],
                            transaction_countries=detail['transaction_countries'],
                            transaction_overview=detail['transaction_overview'],
                            # get_time=detail['get_time'],
                        )
                        # yield detail
                        # print(json.dumps(detail))
                        print('一共有 {0} 个,已经完成了 {1} 个,还有 {2} 个'.format(
                            len(self.start_urls),
                            self.crawler.stats.get_value('cnt'),
                            len(self.start_urls) - self.crawler.stats.get_value('cnt')
                        )
                        )
                        print('公司:{0}'.format(detail['seller']['companyName']))
                        print('完成{0}产品:{1}'.format(item_id, detail['product']['subject']))
                        print('+++++++++++++++++++++++++++++++++++++++++++++===========================')
                        self.crawler.stats.set_value('detail', [])

            except Exception as e:
                print('----------------')
                print('解析详情页出错')
                print(response.request.url)
                print(e)
                print('----------------')
        else:
            print('网络错误')
