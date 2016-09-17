# coding=utf-8
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class TorrentItem(scrapy.Item):
    # 定义您想抓取的数据--实体类
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    size = scrapy.Field()


class MininovaSpider(CrawlSpider):
    name = 'mininova' # 项目名称
    allowed_domains = ['mininova.org'] # domain列表
    start_urls = ['http://www.mininova.org/today'] # 初始 URL
    # 规则http://www.mininova.org/tor/NUMBER，其中，NUMBER 是一个整数 ==>  /tor/\d+
    # parse_torrent 是方法名，由于CrawlSpider使用parse方法来实现其逻辑，所以应避免使用parse作为回调函数，否则规则失效。
    rules = [Rule(LinkExtractor(allow=['/tor/\d+']), 'parse_torrent')]

    def parse_torrent(self, response):
        torrent = TorrentItem()
        torrent['url'] = response.url
        # 下面这些xpath，都是具体抓取页面上的，如http://www.mininova.org/tor/2676093
        torrent['name'] = response.xpath("//h1/text()").extract()
        torrent['description'] = response.xpath("//div[@id='description']").extract()
        torrent['size'] = response.xpath("//div[@id='info-left']/p[2]/text()[2]").extract()
        return torrent

# 运行 spider 来获取网站的数据，并以 JSON 格式存入到 scraped_data.json 文件中:
# scrapy runspider --output=spider_out.json mininova.py
# scrapy 不是内部或外部命令 ==> 配置环境变量即可解决（可以配载用户path下）