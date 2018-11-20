# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
import os
import shutil


class UumtuPipeline(object):
    def process_item(self, item, spider):
        return item

class MoteDownloadPipeline(ImagesPipeline):
    # 使用'/'分割链接，使用最后的部分作为文件名
    def file_path(self, request, response=None, info=None):
        url = request.url
        name_list = url.split('/')
        file_name = name_list[-4] + name_list[-3] + '-' + name_list[-2] + name_list[-1]
        return file_name

    #通过 get_media_requests 方法为每一个图片链接生成请求
    def get_media_requests(self, item, info):
        yield Request(item['url'])

    # 单个 item 完成下载时的处理方法
    def item_completed(self, results, item, info):
        print('=== results: ', results)
        image_paths = [x['path'] for ok, x in results if ok]
        print('== image_paths: ', image_paths)
        if not image_paths:
            raise DropItem('Image Downloaded Failed')

        # 从项目设置文件中导入图片下载路径
        storage = get_project_settings().get('IMAGES_STORE')

        # 定义分类保存路径
        mote_name = item['mote']
        category_name = item['title'].split('第')[0]
        target_path = os.path.join('./mote', mote_name, category_name)
        print('=-= target_path: ', target_path)
        # 若目录不存在则创建目录
        if not os.path.exists(target_path):
            print('--=-- 目录 %s 不存在，开始创建！' % target_path)
            os.makedirs(target_path)

        # 将文件从默认路径移动到指定路径下
        shutil.move(os.path.join(storage, image_paths[0]), os.path.join(target_path, image_paths[0]))

        return item

class XingganDownloadPipeline(ImagesPipeline):
    # 使用'/'分割链接，使用最后的部分作为文件名
    def file_path(self, request, response=None, info=None):
        url = request.url
        name_list = url.split('/')
        file_name = name_list[-4] + name_list[-3] + '-' + name_list[-2] + name_list[-1]
        return file_name

    #通过 get_media_requests 方法为每一个图片链接生成请求
    def get_media_requests(self, item, info):
        yield Request(item['url'])

    # 单个 item 完成下载时的处理方法
    def item_completed(self, results, item, info):
        print('=== results: ', results)
        image_paths = [x['path'] for ok, x in results if ok]
        print('== image_paths: ', image_paths)
        if not image_paths:
            raise DropItem('Image Downloaded Failed')

        # 从项目设置文件中导入图片下载路径
        storage = get_project_settings().get('IMAGES_STORE')

        # 定义分类保存路径
        category_name = item['title'].split('第')[0]
        target_path = os.path.join('./xinggan', category_name)
        print('=-= target_path: ', target_path)
        # 若目录不存在则创建目录
        if not os.path.exists(target_path):
            print('--=-- 目录 %s 不存在，开始创建！' % target_path)
            os.makedirs(target_path)

        # 将文件从默认路径移动到指定路径下
        shutil.move(os.path.join(storage, image_paths[0]), os.path.join(target_path, image_paths[0]))

        return item