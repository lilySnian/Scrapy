# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    # https://movie.douban.com/subject/5045678/
    url = scrapy.Field()
    name = scrapy.Field()
    director = scrapy.Field()   # 导演
    screen_writer = scrapy.Field()   # 编剧
    starring = scrapy.Field()   # 主演
    type = scrapy.Field()   # 类型
    official_website = scrapy.Field()   # 官方网站
    producer_countries_regions = scrapy.Field()   # 制片国家/地区
    language = scrapy.Field()   # 语言
    release_date = scrapy.Field()   # 上映日期
    running_time = scrapy.Field()   # 片长
    also_known_as = scrapy.Field()   # 又名
    imdb_link = scrapy.Field()   # IMDb链接