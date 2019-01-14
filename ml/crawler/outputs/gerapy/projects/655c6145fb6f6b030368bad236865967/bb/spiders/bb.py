from scrapy.spiders import CrawlSpider, Rule
from ..items import *
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings


class BbSpider(CrawlSpider):
    name = "bb"
    allowed_domains = ['bb']
    start_urls = ['bb']
    rules = (
        Rule(LinkExtractor(allow=('bb1')), callback='bb2',
        follow=False
        ),
    )

    def bb2(self, response):

        item = Bb2Item()
        item['bb6'] = self.get_bb6(response)
        yield item

    def get_bb6(self, response):
        bb6 = response.xpath('bb5').extract()
        return bb6[0] if bb6 else ''

