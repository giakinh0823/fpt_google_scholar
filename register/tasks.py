from __future__ import absolute_import, unicode_literals

from celery import shared_task
from .views import getdataArticle,getdataProfile


@shared_task
def getDataCelery():
    getdataProfile()
    getdataArticle()

     

