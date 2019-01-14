from scrapy.spiders import CrawlSpider, Rule
from ..items import *
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings


class Ziru_1Spider(CrawlSpider):
    name = "ziru_1"
    allowed_domains = ['www.ziroom.com']
    start_urls = ['http://www.ziroom.com/z/nl/z2-d23008614.html']
    rules = (
        Rule(LinkExtractor(allow=('/z/vr/\d+\.html')), callback='parse_room',
        follow=False
        ),
    )

    def parse_room(self, response):
        item = RoomItem()
        item['price'] = self.get_price(response)
        item['name'] = self.get_name(response)
        yield item

    def get_price(self, response):
        price = response.xpath('//span[@class="ellipsis"]/text()').extract()
        return price[0] if price else ''

    def get_name(self, response):
        name = response.xpath('//span[@class="ellipsis"]/text()').extract()
        return name[0] if name else ''

