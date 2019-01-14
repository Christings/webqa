from scrapy.spiders import CrawlSpider, Rule
from ..items import *
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings


class NihSpider(CrawlSpider):
    name = "nih"
    allowed_domains = ['ww']
    start_urls = ['ww']
    rules = (
        Rule(LinkExtractor(allow=('ww')), callback='ww',
        follow=False
        ),
    )

    def ww(self, response):

        item = WwItem()
        item['ww'] = self.get_ww(response)
        yield item

    def get_ww(self, response):
        ww = response.xpath('ww').extract()
        return ww[0] if ww else ''

