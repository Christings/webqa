import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from xd.spiders.xd import XdSpider


process = CrawlerProcess(get_project_settings())
process.crawl(XdSpider)
process.start()
