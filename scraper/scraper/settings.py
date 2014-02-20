BOT_NAME = 'scraper'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'
# Allow all domain
SPIDER_MIDDLEWARES = {
    'scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware': None,
}
# Delay download
DOWNLOAD_DELAY = 1
DUPEFILTER_CLASS = 'scrapy.dupefilter.BaseDupeFilter'
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
RANDOM_DOWNLOAD_DELAY = False
import sys
import os

sys.path.append('../../search_hotel_base_on_request')
# DJANGO SETTING
os.environ['DJANGO_SETTINGS_MODULE'] = 'search_hotel_base_on_request.settings'

