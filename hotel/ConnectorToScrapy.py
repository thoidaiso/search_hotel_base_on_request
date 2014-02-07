from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from scraper.scraper.spiders.hotel_spider import HotelSpider

class ConnectorToScrapy:
    def stop_reactor():
        reactor.stop()
    
    def run_spider(self, dict):  
        
        Spider = dict.get('spider', None)
        args = dict.get('args', [])
        
        argument=[]
        spider = Spider(args)
        settings = get_project_settings()
        crawler = Crawler(settings)
        crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()
        log.start()
        reactor.run()