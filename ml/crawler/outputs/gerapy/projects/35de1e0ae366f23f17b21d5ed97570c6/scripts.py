import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from xx.spiders.xx import XxSpider


process = CrawlerProcess(get_project_settings())
process.crawl(XxSpider)
process.start()
