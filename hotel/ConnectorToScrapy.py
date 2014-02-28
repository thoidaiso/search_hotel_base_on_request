
from multiprocessing import Process
from scrapy.crawler import CrawlerProcess
from scrapy.settings import CrawlerSettings, Settings
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from scraper.scraper.spiders.agoda_spider import AgodaSpider
from scraper.scraper.spiders.ivivu_spider import IvivuSpider
from importlib import import_module
from datetime import datetime, timedelta

#search from today+day1 to today+day2
def crawl_spider(domain, day1, day2):
    spider_dict ={'agoda.com': AgodaSpider, 'ivivu.com': IvivuSpider}
    
    args = {'from_date': datetime.now() + timedelta(days=day1),
            'to_date'  : datetime.now() + timedelta(days=day2)
        }
    
    print "\n crawl spider==========="
 
    spider = spider_dict.get(domain, AgodaSpider)
    spider = spider(args)
        
    settings_module = import_module('scraper.scraper.settings')
    settings = CrawlerSettings(settings_module)
    settings.overrides['SPIDER_MODULES'] = ['scraper.scraper.spiders']
    
#        settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start()
    reactor.run()
