from scrapy.spiders import CrawlSpider, Rule
from ..items import *
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings


class XxSpider(CrawlSpider):
    name = "xx"
    allowed_domains = ['xx']
    start_urls = ['xx']
    rules = (
        Rule(LinkExtractor(allow=('xx1')), callback='xx2',
        follow=False
        ),
    )

    def xx2(self, response):

        item = Xx2Item()
        item['xx4'] = self.get_xx4(response)
        item['zz6'] = self.get_zz6(response)
        yield item

    def get_xx4(self, response):
        xx4 = response.xpath('xx3').extract()
        return xx4[0] if xx4 else ''

    def get_zz6(self, response):
        zz6 = response.xpath('xx5').extract()
        return zz6[0] if zz6 else ''

