# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from uumtu.utils import get_config
from uumtu.rules import rules
from uumtu.items import XingganItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose

class PicsLoader(ItemLoader):
    default_output_processor = TakeFirst()

class XingganLoader(PicsLoader):
    text_out = Compose(Join(), lambda s: s.strip())
    source_out = Compose(Join(), lambda s: s.strip())

class UniversalSpider(CrawlSpider):
    name = 'universal'

    def __init__(self, name, *args, **kwargs):
        config = get_config(name)
        print('---- config:', config)
        self.config = config
        self.rules = rules.get(config.get('rules'))
        self.start_urls = config.get('start_urls')
        self.allowed_domains = config.get('allowed_domains')
        super(UniversalSpider, self).__init__(*args, **kwargs)


    def parse_item(self, response):
        item = self.config.get('item')
        if item:
            cls = eval(item.get('class'))()
            loader = eval(item.get('loader'))(cls, response=response)
            # 动态获取属性配置
            for key, value in item.get('attrs').items():
                for extractor in value:
                    if extractor.get('method') == 'xpath':
                        loader.add_xpath(key, *extractor.get('args'), **{'re': extractor.get('re')})
                    if extractor.get('method') == 'css':
                        loader.add_css(key, *extractor.get('args'), **{'re': extractor.get('re')})
                    if extractor.get('method') == 'value':
                        loader.add_value(key, *extractor.get('args'), **{'re': extractor.get('re')})
                    if extractor.get('method') == 'attr':
                        loader.add_value(key, getattr(response, *extractor.get('args')))
        yield loader.load_item()