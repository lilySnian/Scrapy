# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor, re

from items import MovieItem

class MininovaSpider(CrawlSpider):
    name = "movie"
    allowed_domains = ['movie.douban.com']  # domain列表

    # 任意和包含电影url的页面，如https://movie.douban.com(错误start_urls：https://movie.douban.com/)，或者如下url
    start_urls = ['https://movie.douban.com/subject/5327268/']

    # 自动提取某页面符合要求的url，并将结果存储到url队列中，待抓取：
    # 1、规则例子：https://movie.douban.com/subject/26284595/?from=showing
    # 2、注意：由于CrawlSpider使用parse方法来实现其逻辑，所以应避免使用parse作为回调函数，否则规则失效
    rules = [Rule(LinkExtractor(allow=['/subject/\d+']), process_links='link_filtering', callback='parse_movie', follow=True)]

    def link_filtering(self, links):
        # url过滤:
        # links:[Link(url='https://movie.douban.com/subject/26303622/?from=subject-page', text=u'\u66f4\u591a', fragment='', nofollow=False), ...]
        # 1、 提取url：
        #   a、url位置，link.url:'https://movie.douban.com/subject/26303622/photos?type=R'
        #   b、利用正则提取需要的url,如'https://movie.douban.com/subject/26303622/photos?type=R' -> 'https://movie.douban.com/subject/26303622'
        #
        # 2、将过滤结果返回给scrapy
        #   link.url = url，替换url
        #   ret.append(link) 将过滤结果存储到新的list中
        #   最后将新结果返回给scrapy
        ret = []
        r = re.compile("https://movie.douban.com/subject/\d+")
        for link in links:
            parsed_url = link.url
            if r.search(parsed_url):
                url = r.search(parsed_url).group()
                link.url = url
                ret.append(link)
        return ret  # 将过滤结果返回给scrapy


    def parse_movie(self, response):
        # 提取电影介绍页面信息（如，https://movie.douban.com/subject/5045678/）:
        # string(.):提取某标签下所有的文字，包括子标签内的内容,具体见http://scrapy-chs.readthedocs.io/zh_CN/latest/topics/selectors.html--Some XPath tips
        # extract():提取的是list，所以获取第一个结果

        movie = MovieItem()
        # 提取url
        movie['url'] = response.url
        # 提取名字
        movie['name'] = response.xpath("string(//div[@id='wrapper']/div[@id='content']/h1/span[1])").extract()[0]
        # 提取导演
        movie['director'] = response.xpath("string(//div[@id='info']/span[1]/span[@class='attrs'])").extract()[0]
        # 提取编剧
        movie['screen_writer'] = response.xpath("string(//div[@id='info']/span[2]/span[@class='attrs'])").extract()[0]
        # 提取主演
        movie['starring'] = response.xpath("string(//div[@id='info']/span[@class='actor']/span[@class='attrs'])").extract()[0]
        # 提取类型--多个标签
        type = response.xpath("string(//div[@id='info']/span[5])").extract()[0]
        type += ("/" + response.xpath("string(//div[@id='info']/span[6])").extract()[0])
        type += ("/" + response.xpath("string(//div[@id='info']/span[7])").extract()[0])
        movie['type'] = type
        # 提取官方网站
        movie['official_website'] = response.xpath("string(//div[@id='info']/a[1])").extract()[0]
        # 提取制片国家/地区
        movie['producer_countries_regions'] = response.xpath("string(//*[@id='info']/text()[11])").extract()[0]
        # 提取语言
        movie['language'] = response.xpath("string(//*[@id='info']/text()[13])").extract()[0]
        # 提取上映日期
        movie['release_date'] = response.xpath("string(//div[@id='info']/span[12])").extract()[0]
        # 提取片长
        movie['running_time'] = response.xpath("string(//div[@id='info']/span[14])").extract()[0]
        # 提取又名
        movie['also_known_as'] = response.xpath("string(//*[@id='info']/text()[19])").extract()[0]
        # 提取IMDb链接
        movie['imdb_link'] = response.xpath("string(//div[@id='info']/a[2])").extract()[0]

        # print movie['url']
        # print movie['name']
        # print movie['director'].encode('utf-8')
        # print movie['official_website'].encode('utf-8')
        # print movie['starring'].encode('utf-8')
        # print movie['type']
        # print movie['official_website'].encode('utf-8')
        # print movie['producer_countries_regions']
        # print movie['language'].encode('utf-8')
        # print movie['release_date'].encode('utf-8')
        # print movie['running_time'].encode('utf-8')
        # print movie['also_known_as'].encode('utf-8')
        # print movie['imdb_link'].encode('utf-8')

        yield movie





