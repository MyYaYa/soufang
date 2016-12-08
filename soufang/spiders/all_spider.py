# -*- coding: utf-8 -*-

import scrapy
import re
from urllib.parse import urlencode
from soufang.items import SoufangItem

class SoufangSpider(scrapy.Spider):
    name = "soufangall"
    start_urls = ["http://esf.fang.com/newsecond/esfcities.aspx"]

    def parse(self, response):
        lis = response.xpath('//*[@id="c02"]/ul/li')
        for x in lis:
            if x.xpath('strong/text()').extract_first() != '其他':
                cities = x.xpath('child::a')
                for city in cities:
                    if city.xpath('text()').extract_first() != '北京' and city.xpath('text()').extract_first() != '上海':
                        # print(city.xpath('text()').extract_first())
                        yield scrapy.Request(url=city.xpath('@href').extract_first()+'/housing/', callback=self.parse_city)

    def parse_city(self, response):
        ds = response.xpath('//*[@id="houselist_B03_02"]/div[1]/a')
        for d in ds[1:]:
            district_url = d.xpath('@href').extract_first().split('/')[-2]
            yield scrapy.Request(url=response.url+district_url+'/', callback=self.parse_district)

    def parse_district(self, response):
        streets = response.xpath('//*[@id="shangQuancontain"]/a')
        for s in streets[1:]:
            street_url = s.xpath('@href').extract_first()
            s_url = '/'.join(response.url.split('/')[0:-3])+street_url
            yield scrapy.Request(url=s_url, callback=self.parse_com)


    def parse_com(self, response):
        next_a_text = response.xpath('//div[@class="fanye gray6"]/a[last()-1]/text()').extract_first()
        if next_a_text == '下一页':
            next_a_href = response.xpath('//div[@class="fanye gray6"]/a[last()-1]/@href').extract_first()
            next_url = '/'.join(response.url.split('/')[:-3]) + next_a_href
            yield scrapy.Request(url=next_url, callback=self.parse_com)

        for x in response.xpath('//div[@class="list rel"]/dl/dd/p[1]'):
            if x.xpath('span/text()').extract_first() == '住宅' or '别墅':
                url = x.xpath('a/@href').extract_first()
                if url:
                    yield scrapy.Request(url=url, callback=self.parse_little)

    def parse_little(self, response):
        item = SoufangItem()
        item["city"] = response.xpath('//*[@id="dsy_H01_01"]/div[1]/a/text()').extract_first()
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
        item["source"] = "soufang"
        item["title"] = response.xpath('//h1/a/text()').extract_first()[0:-3]
        item["district"] = response.xpath('//dd/strong[text()="所属区域："]/../text()').extract_first()
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
        city_ju = item["city"].encode('unicode-escape').decode('utf-8').replace('\\', '%')
        url = "http://fangjia.fang.com/pinggu/ajax/ChartAjaxContainMax.aspx?dataType=proj&city=%s&KeyWord=%s&year=1" % (city_ju, item["internal_id"])
        try:
            request = scrapy.Request(url=url, callback=self.parse_price)
        except:
            return item
        request.meta['item'] = item
        return request

    def parse_price(self, response):
        item = response.meta['item']
        try:
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
        finally:
            return item
