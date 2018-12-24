from scrapy import cmdline

cmd="scrapy crawl " + ${project.name}
cmdline.execute(cmd.split(' '))