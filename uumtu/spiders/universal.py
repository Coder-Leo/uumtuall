# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from uumtu.utils import get_config
from uumtu.rules import rules


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
        i = {}
        return i
