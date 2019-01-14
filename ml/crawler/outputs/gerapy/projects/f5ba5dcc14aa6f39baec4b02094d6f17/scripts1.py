import sys

from twisted.internet import reactor
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from xd.spiders.xd import XdSpider

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='log.txt',
    format='%(levelname)s:%(message)s',
    level=logging.INFO
)

runner = CrawlerRunner(get_project_settings())
d=runner.crawl(XdSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run()
