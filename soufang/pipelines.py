# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
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
        engine = create_engine('mysql+pymysql://%s:%s@%s:3306/%s?charset=utf8' %
            (self.config.get('user'), self.config.get('password'), self.config.get('host'), self.config.get('db')))
        DBsession = sessionmaker(bind=engine)
        self.session = DBsession()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        com = self.session.query(Community).filter(and_(Community.source == item["source"], Community.internal_id == item["internal_id"])).first()
        if not com:
            com_id = str(uuid.uuid1())
            com = Community(id = com_id,
                            source = item["source"],
                            title = item["title"],
                            internal_id = item["internal_id"],
                            district = item["district"],
                            address = item["address"],
                            unit_price = item["unit_price"],
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
            cph = self.session.query(CommunityPriceHistory).filter(and_(CommunityPriceHistory.community_id == com.id,
                                                                CommunityPriceHistory.month == k)).first()
            if not cph:
                price_id = str(uuid.uuid1())
                p = CommunityPriceHistory(id = price_id,
                                        source = item["source"],
                                        community_id = com.id,
                                        month = k,
                                        price = v,)
                self.session.add(p)

        self.session.commit()
        return item
