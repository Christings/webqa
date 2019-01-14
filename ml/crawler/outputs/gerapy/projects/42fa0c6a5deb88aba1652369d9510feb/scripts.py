import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from ziru_1.spiders.ziru_1 import Ziru_1Spider


process = CrawlerProcess(get_project_settings())
process.crawl(Ziru_1Spider)
process.start()
