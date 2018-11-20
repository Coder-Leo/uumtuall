# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from uumtu.utils import get_config
from uumtu.rules import rules
from uumtu.items import XingganItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose
from uumtu import urls

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
        start_urls = config.get('start_urls')
        if start_urls:
            if start_urls.get('type') == 'static':
                self.start_urls = start_urls.get('value')
            elif start_urls.get('type') == 'dynamic':
                self.start_urls = list(eval('urls.' + start_urls.get('method'))(*start_urls.get('args', [])))
        self.allowed_domains = config.get('allowed_domains')
        super(UniversalSpider, self).__init__(*args, **kwargs)


    def parse_item(self, response):
        print('====== response: ', response)
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

        # 生成该mote的指定专辑中的所有图的连接请求
        atext = response.xpath('//div[contains(@class, "page")]//a[last()]/text()').extract_first()
        if atext == '末页':
            # print('--- 该专辑存在‘末页’。继续请求下一张图')
            nexturl = response.xpath('//div[contains(@class, "page")]//a[last() - 1]/@href').extract_first()
            # print('---- 下一张图的url:', nexturl)
            yield response.follow(nexturl, self.parse_item)
        else:
            print('-- 该专辑没有下一张图了！ --')