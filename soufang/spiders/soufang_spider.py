# -*- coding: utf-8 -*-

import scrapy
import re
from soufang.items import SoufangItem

class SoufangSpider(scrapy.Spider):
    name = "soufang"
    districts = {'chaoyang':'1', 'haidian':'0', 'fengtai':'6',
        'dongcheng':'2', 'xicheng':3, 'shijingshan':7,
        'changping':'12', 'daxing':585, 'tongzhou':10,
        'shunyi':'11', 'fangshan':'8', 'miyun':'13',
        'mentougou':'9', 'huairou':'14', 'yanqing':15,
        'pinggu':'16', 'yanjiao':'987', 'beijingzhoubian':'11817'}
    start_urls = ["http://esf.fang.com/housing/%s__%s_0_0_0_1_0_0" % (y, n) for (x,y) in districts.items() for n in ['1','2']]

    def parse(self, response):
        next_a_text = response.xpath('//div[@class="fanye gray6"]/a[last()-1]/text()').extract_first()
        if next_a_text == '下一页':
            next_a_href = response.xpath('//div[@class="fanye gray6"]/a[last()-1]/@href').extract_first()
            next_url = "http://esf.fang.com" + next_a_href
            yield scrapy.Request(url=next_url, callback=self.parse)

        for a_href in response.xpath('//div[@class="list rel"]/dl/dd/p[1]/a/@href'):
            url = a_href.extract()
            if url:
                yield scrapy.Request(url=url, callback=self.parse_little)

    def parse_little(self, response):
        item = SoufangItem()
        item["property"]= response.xpath('//li/strong[text()="物业公司："]/../text()').extract_first()
        item["total_buildings"] = response.xpath('//li/strong[text()="楼栋总数："]/../text()').extract_first()
        src = response.xpath('//div[@class="con_left"]/div[2]/iframe/@src').extract_first()
        code = src.split('/')[5].split('?')[1].split('&')[0].split('=')[1]
        item["internal_id"] = code
        request = scrapy.Request(url=(response.url + "xiangqing/"), callback=self.parse_info)
        request.meta['item'] = item
        return request

    def parse_info(self, response):
        item = response.meta['item']
        item["title"] = response.xpath('//h1/a/text()').extract_first()[0:-3]
        item["address"] = response.xpath('//dd/strong[text()="小区地址："]/../text()').extract_first()
        item["unit_price"] = response.xpath('//dl/dt[text()="本月均价"]/../dd/span/text()').extract_first()
        item["build_time"] = response.xpath('//dd/strong[text()="竣工时间："]/../text()').extract_first()
        item["build_type"] = response.xpath('//dd/strong[text()="建筑类别："]/../text()').extract_first()
        item["property_fee"] = response.xpath('//dd/strong[text()="物 业 费："]/../text()').extract_first()
        item["developer"] = response.xpath('//dd/strong[text()="开 发 商："]/../text()').extract_first()
        item["total_houses"] = response.xpath('//dd/strong[text()="总 户 数："]/../text()').extract_first()
        item["plot_rate"] = response.xpath('//dd/strong[text()="容 积 率："]/../text()').extract_first()
        item["green_rate"] = response.xpath('//dd/strong[text()="绿 化 率："]/../text()').extract_first()
        item["parking_num"] = response.xpath('//dt/strong[text()="停 车 位："]/../text()').extract_first()
        url = "http://fangjia.fang.com/pinggu/ajax/ChartAjaxContainMax.aspx?dataType=proj&city=%%u5317%%u4EAC&KeyWord=%s&year=1" % item["internal_id"]
        request = scrapy.Request(url=url, callback=self.parse_price)
        request.meta['item'] = item
        return request

    def parse_price(self, response):
        item = response.meta['item']
        b = response.body
        s = str(b)
        data = s.split('&')[0].split("'")[1]
        pattern = re.compile(',([0-9]+)]')
        match = pattern.findall(data)
        months = ['201512','201601','201602','201603','201604','201605','201606','201607','201608','201609','201610','201611']
        if match:
            length = len(match)
            prices = {}
            for x in range(0, length):
                prices[months[12-length+x]] = match[x]
            item["prices"] = prices
        return item
