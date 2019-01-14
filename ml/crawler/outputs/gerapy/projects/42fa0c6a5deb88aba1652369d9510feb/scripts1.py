import sys
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess,CrawlerRunner
from scrapy.utils.log import configure_logging
import logging
from scrapy.utils.project import get_project_settings
from ziru_1.spiders.ziru_1 import Ziru_1Spider

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='log.txt',
    format='%(levelname)s:%(message)s',
    level=logging.INFO
)

runner = CrawlerRunner(get_project_settings())
d=runner.crawl(Ziru_1Spider)
# d=runner.join()
d.addBoth(lambda _: reactor.stop())
reactor.run()
