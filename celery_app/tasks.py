from __future__ import absolute_import
from celery import task
from celery.schedules import crontab
from celery.task import periodic_task
from datetime import datetime, timedelta
from hotel.models import Price_Book

#search hotel from today+day1 to today+day2
@task()
def crawl_spider(args):
    domain = args.get('domain', 'agoda.com')
    day1 = args.get('day1', 1)
    day2 = args.get('day2', 3)
    
    print "\n crawl spider from celery", domain,';;day1==',day1,';;day2==',day2
    from hotel.ConnectorToScrapy import crawl_spider
    return crawl_spider(domain, day1, day2)



#@periodic_task(run_every=crontab(hour=15, minute=22))
##delete price book record which have date_end less than today
@task()
def delete_old_price_book_data():
    print "\n delete price book record which have date_end less than today"
    today = datetime.now()
    Price_Book.objects.filter(date_end__lte = today).delete()
    
