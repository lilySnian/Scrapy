# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs # 编码
import json

# 将结果以json格式写入文件
class MoviePipeline(object):
    def __init__(self):
        # codecs：可以处理大部分写入字符串乱码问题
        self.file = codecs.open('douban_movie.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        if item['name'] != '' and item['name'] != None and len(item['name']) > 0:
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'
            self.file.write(line)
            return item
        else:
            return None

    def spider_closed(self, spider):
        # 关闭IO
        self.file.close()
