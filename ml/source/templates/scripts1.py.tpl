import sys

from twisted.internet import reactor
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from ${project.name}.spiders.${project.name} import ${project.name.capitalize()}Spider

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='log.txt',
    format='%(levelname)s:%(message)s',
    level=logging.INFO
)

runner = CrawlerRunner(get_project_settings())
d=runner.crawl(${project.name.capitalize()}Spider)
d.addBoth(lambda _: reactor.stop())
reactor.run()
