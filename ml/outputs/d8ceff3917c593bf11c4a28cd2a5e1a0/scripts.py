import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from douban1.spiders.douban1 import Douban1Spider


process = CrawlerProcess(get_project_settings())
process.crawl(Douban1Spider)
process.start()
