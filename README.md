search_hotel_base_on_request
============================

Django part of Project.
This is frontend of Prject.
Backend is scrapy



###Install celery and djcelery
pip install Celery
pip install django-celery

#Install flower for web-monitor
pip install flower

#Install RabbitMQ
sudo apt-get install rabbitmq-server


#MIgrate database celery
python manage.py migrate djcelery

#Run celery

--------Run worker and beat(scheduler)

/search_hotel_base_on_request$ celery -A search_hotel_base_on_request worker  -l info -B 



---Run celery web monitor, we will have a web monitor at localhost:5555

/search_hotel_base_on_request$ celery flower




----Run celery cam to save data about task like time... in database

/search_hotel_base_on_request$ python manage.py celerycam
