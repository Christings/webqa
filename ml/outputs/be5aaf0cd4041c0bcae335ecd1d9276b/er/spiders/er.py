from scrapy.spiders import CrawlSpider, Rule
from ..items import *
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings


class ErSpider(CrawlSpider):
    name = "er"
    allowed_domains = ['wfe']
    start_urls = ['wef']
    rules = (
        Rule(LinkExtractor(allow=('we')), callback='wfe',
        follow=False
        ),
    )

    def wfe(self, response):
        item = WfeItem()
        yield item

