import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from bb.spiders.bb import BbSpider


process = CrawlerProcess(get_project_settings())
process.crawl(BbSpider)
process.start()
