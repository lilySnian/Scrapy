# coding=utf-8
import scrapy


class DmozItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()


class DmozSpider(scrapy.spiders.Spider):
    # 类的三个属性:
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/"
    ]

    # Spider唯一的方法
    def parse(self, response):
        filename = response.url.split("/")[-2] # Resources  Books

        # 下载start_urls中url的页面，并存储到Resources、Books中
        with open(filename, 'wb') as f:
            f.write(response.body)

        # 提取内容
        # 这里需要空格'//*[@id="site-list-content"]//div[@class="site-item "]'
        for sel in response.xpath('//*[@id="site-list-content"]//div[@class="site-item "]'):
            item = DmozItem()
            item['title'] = sel.xpath('div[3]/a/div/text()').extract()
            item['link'] = sel.xpath('div[3]/a/@href').extract()
            item['desc']= sel.xpath('div[3]/div/text()').extract()
            yield item

# scrapy runspider  dmoz.py

