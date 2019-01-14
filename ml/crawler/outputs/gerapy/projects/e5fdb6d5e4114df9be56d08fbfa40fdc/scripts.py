import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from cc.spiders.cc import CcSpider


process = CrawlerProcess(get_project_settings())
process.crawl(CcSpider)
process.start()
