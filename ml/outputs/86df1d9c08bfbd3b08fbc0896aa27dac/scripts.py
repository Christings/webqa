import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from douban2.spiders.douban2 import Douban2Spider


process = CrawlerProcess(get_project_settings())
process.crawl(Douban2Spider)
process.start()
