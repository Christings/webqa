import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from nih.spiders.nih import NihSpider


process = CrawlerProcess(get_project_settings())
process.crawl(NihSpider)
process.start()
