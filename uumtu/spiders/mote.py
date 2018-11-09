# -*- coding: utf-8 -*-
from scrapy import Spider, Request
import re
from uumtu.items import MoteItem

class MoteSpider(Spider):
    name = 'mote'
    allowed_domains = ['uumtu.com']
    start_urls = ['https://uumtu.com/mote/']

    def parse(self, response):
        '''
        生成当前页面的模特列表中每个mote的链接请求
        '''
        mote_url_list = response.xpath('//div[@class="mote-warp mt14 mote-list"][1]//li/a/@href').extract()
        # print('# mote list:', mote_url_list)
        mote_name_list = response.xpath('//div[@class="mote-warp mt14 mote-list"][1]//li/a/text()').extract()
        # print('## mote name list:', mote_name_list)
        mote_data = dict(zip(mote_name_list, mote_url_list))
        # print('### mote data:', mote_data)

        # 生成每一个mote的链接请求
        for mote, url in mote_data.items():
            print('模特：%s= %s' % (mote, url))
            yield response.follow(url, self.parse_single_mote, meta={"name": mote})

        '''
        生成mote专区所有页面的链接请求
        '''
        base_url = "https://www.uumtu.com/mote/1-0-0-0/{}.html"
        atext = response.xpath('//div[contains(@class, "page")]//a[last()]/text()').extract_first()
        if atext == '末页':
            print('--- 存在‘末页’。继续请求下一页')
            nextpage = int(response.xpath('//div[contains(@class, "page")]//a[last() - 1]/@href').extract_first().split('/')[-1].split('.')[0])
            print('---- 第 %s 页 ----' % nextpage)
            url = base_url.format(nextpage)
            print('-=-=-= url:', url)
            yield Request(url, self.parse)
        else:
            print('-- 没有更多mote了！ --')

    def parse_single_mote(self, response):
        # cookie = response.headers.getlist('Set-Cookie')
        # print('&& cookie:', cookie)

        mote_name = response.meta['name']
        print('--- mote name:', mote_name)
        '''
        生成该mote的所有最新专辑列表页面中的连接请求
        '''
        atext = response.xpath('//div[contains(@class, "page")]//a[last()]/text()').extract_first()
        if atext == '末页':
            # print('--- 该mote存在‘末页’。继续请求下一专辑列表页面')
            nexturl = response.xpath('//div[contains(@class, "page")]//a[last() - 1]/@href').extract_first()
            # print('---- 下一专辑列表页面的url:', nexturl)
            yield response.follow(nexturl, self.parse_single_mote)
        else:
            print('-- 该mote没有更多专辑列表了！ --')

        '''
        生成该mote所有专辑入口的链接请求
        '''
        all_categories_src = response.xpath('//div[@class="warp mote-list-body clearfix"]//dl/dd/a/@href').extract()
        category_title = response.xpath('//div[@class="warp mote-list-title clearfix"]/h2/text()').extract_first()
        data = {"src": all_categories_src, "title": category_title}
        # print('=== data: ', data)

        for src in all_categories_src:
            print('=== 专辑入口的链接: ', src)
            yield response.follow(src, self.parse_single_cate, meta={"name": mote_name})

    def parse_single_cate(self, response):
        meta = response.meta
        print('--- --- meta:', meta)
        mote_name = meta['name']

        current_src = response.xpath('//div[contains(@class, "imgac")]/a/img/@src').extract_first()
        current_title = response.xpath('//div[contains(@class, "imgac")]/a/img/@alt').extract_first()
        data = {"src": current_src, "title": current_title}
        # print('=== data: ', data)

        # 生成这张图的item
        item = MoteItem()
        item['mote'] = mote_name
        item['url'] = current_src
        item['title'] = current_title
        yield item

        # 生成该mote的指定专辑中的所有图的连接请求
        atext = response.xpath('//div[contains(@class, "page")]//a[last()]/text()').extract_first()
        if atext == '末页':
            # print('--- 该专辑存在‘末页’。继续请求下一张图')
            nexturl = response.xpath('//div[contains(@class, "page")]//a[last() - 1]/@href').extract_first()
            # print('---- 下一张图的url:', nexturl)
            yield response.follow(nexturl, self.parse_single_cate, meta={"name": mote_name})
        else:
            print('-- 该专辑没有下一张图了！ --')