import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from er.spiders.er import ErSpider


process = CrawlerProcess(get_project_settings())
process.crawl(ErSpider)
process.start()
