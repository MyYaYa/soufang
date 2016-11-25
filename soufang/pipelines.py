# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .orm.entity import *
import uuid

class SoufangPipeline(object):
    def __init__(self, config):
        self.config = config

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            config = crawler.settings.get('DB_CONFIG')
        )

    def open_spider(self, spider):
        engine = create_engine('mysql+pymysql://%s:%s@localhost:3306/%s?charset=utf8' %
            (self.config.get('user'), self.config.get('password'), self.config.get('db')))
        DBsession = sessionmaker(bind=engine)
        self.session = DBsession()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        com_id = str(uuid.uuid1())
        com = Community(id = com_id,
                        source = "soufang",
                        title = item["title"],
                        internal_id = item["internal_id"],
                        address = item["address"],
                        # unit_price = item["unit_price"],
                        # prices = repr(item["prices"]),
                        total_buildings = item["total_buildings"],
                        total_houses = item["total_houses"],
                        build_type = item["build_type"],
                        build_time = item["build_time"],
                        developer = item["developer"],
                        property = item["property"],
                        property_fee = item["property_fee"],
                        parking_num = item["parking_num"],
                        green_rate = item["green_rate"],
                        plot_rate = item["plot_rate"],)
        self.session.add(com)

        for (k,v) in item["prices"].items():
            price_id = str(uuid.uuid1())
            p = CommunityPriceHistory(id = price_id,
                                    community_id = com_id,
                                    month = k,
                                    price = v,)
            self.session.add(p)

        self.session.commit()
        return item
