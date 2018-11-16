# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from uumtu.items import XingganItem

class XingganSpider(CrawlSpider):
    name = 'xinggan'
    allowed_domains = ['uumtu.com']
    start_urls = ['https://www.uumtu.com/xinggan/list_1.html']

    rules = (
        Rule(LinkExtractor(allow='xinggan\/.*\.html',restrict_xpaths='//div[@id="mainbodypul"]//a'), callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths='//div[contains(@class, "both")]//a[contains(., "下一页")]'))
    )

    def parse_item(self, response):

        atext = response.xpath('//div[contains(@class, "page")]//a[last()]/text()').extract_first()
        if atext == '末页':
            print('--- 该mote存在‘末页’。继续请求下一图片页面')
            nexturl = response.xpath('//div[contains(@class, "page")]//a[last() - 1]/@href').extract_first()
            print('---- 下一图片页面的url:', nexturl)
            yield response.follow(nexturl, self.parse_item)
        else:
            print('-- 该mote没有更多专辑列表了！ --')

        item = XingganItem()
        item['url'] = response.xpath('//div[contains(@class, "imgac")]/a/img/@src').extract_first()
        item['title'] = response.xpath('//div[contains(@class, "imgac")]/a/img/@alt').extract_first()
        item['website'] = "优优美图"
        print('--- item: ---', item)
        yield item
