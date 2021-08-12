from __future__ import absolute_import, unicode_literals

from celery import shared_task
from Scholar.getDataScholarUpdate import data_profile, data_scrap
from .models import UserProfile
from Scholar.celery import app
import logging


import nltk
nltk.download('stopwords') #if can't not run please remove comment in here
nltk.download('punkt') #if can't not run please remove comment in here
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk import pos_tag

logger = logging.getLogger(__name__)


def getDataProfile():
    az = 'fpt+university'
    # str = 'fpt+university'
    profiles = UserProfile.objects.all();
    page = len(profiles)
    while page % 10 !=0:
        page -= 1
    number = str(page) 
    data_profile('https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors='+ az +'&astart='+number)
    
def getDataArticle():
    profiles = UserProfile.objects.all()
    for profile in profiles:
        print("Update article profile: "+ profile.name)
        if 'scholar.google.com' in str(profile.homepage):
            data_scrap(profile.homepage, profile.user)

@app.task(name="get_data_article_child", bind=True, max_retries=3)
def getDataArticleChild(self,homepage, userid):
    try:
        data_scrap(homepage, userid)
    except Exception as ex:
        logger.exception(ex)
        self.retry(countdown=3**self.request.retries)


@shared_task(name="get_data")
def getDataCelery():
    getDataProfile()
    getDataArticleCelery()

@shared_task(name="get_data_article")
def getDataArticleCelery():
    profiles = UserProfile.objects.all()
    for profile in profiles:
        print("Update article profile: "+ profile.name)
        if 'scholar.google.com' in str(profile.homepage):
            getDataArticleChild.delay(profile.homepage, profile.user.id)
    
    
@app.task(name="get_data_profile", bind=True, max_retries=3)
def getDataProfileCelery(self):
    try:
        getDataProfile()
    except Exception as ex:
        logger.exception(ex)
        self.retry(countdown=3**self.request.retries)


     

