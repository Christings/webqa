from scrapy.spiders import CrawlSpider, Rule
from ..items import *
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings


class Douban2Spider(CrawlSpider):
    name = "douban2"
    allowed_domains = ['www.douban.com']
    start_urls = ['https://www.douban.com/group/haixiuzu/discussion']
    rules = (
        Rule(LinkExtractor(allow=('/group/\w+/discussion\?start=[0-9]{0,4}$')), callback='',
        follow=True
        ),
        Rule(LinkExtractor(allow=('/group/topic/\d+/')), callback='parse_topic',
        follow=False
        ),
    )

    def parse_topic(self, response):
        item = TopicItem()
        yield item

