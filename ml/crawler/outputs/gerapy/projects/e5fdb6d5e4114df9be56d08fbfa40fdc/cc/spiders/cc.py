from scrapy.spiders import CrawlSpider, Rule
from ..items import *
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings


class CcSpider(CrawlSpider):
    name = "cc"
    allowed_domains = ['cc']
    start_urls = ['cc']
    rules = (
        Rule(LinkExtractor(allow=('cc1')), callback='cc2',
        follow=False
        ),
    )

    def cc2(self, response):

        item = Cc2Item()
        item['cc6'] = self.get_cc6(response)
        yield item

    def get_cc6(self, response):
        cc6 = response.xpath('cc5').extract()
        return cc6[0] if cc6 else ''

