from scrapy.spiders import CrawlSpider, Rule
from ..items import *
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings


class XdSpider(CrawlSpider):
    name = "xd"
    allowed_domains = ['dw']
    start_urls = ['dw']
    rules = (
        Rule(LinkExtractor(allow=('dw')), callback='qwd',
        follow=False
        ),
    )

    def qwd(self, response):

        item = QwdItem()
        item['dw'] = self.get_dw(response)
        yield item

    def get_dw(self, response):
        dw = response.xpath('qwd').extract()
        return dw[0] if dw else ''

