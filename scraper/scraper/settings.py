# Scrapy settings for scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scraper'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'
# Allow all domain
SPIDER_MIDDLEWARES = {
    'scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware': None,
}
# Delay download
DOWNLOAD_DELAY = 1
DUPEFILTER_CLASS = 'scrapy.dupefilter.BaseDupeFilter'

import sys
sys.path.append('/home/sepdau/Dropbox/search_hotel_base_on_request')

# DJANGO SETTING
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'search_hotel_base_on_request.settings'