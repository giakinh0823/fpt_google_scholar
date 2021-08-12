from __future__ import absolute_import, unicode_literals

from celery import shared_task
import re
from article.models import Article
from django.contrib.auth.models import User
from datetime import date
from Scholar.getDataScholar import data_profile, data_scrap
from .models import *

import nltk
nltk.download('stopwords') #if can't not run please remove comment in here
nltk.download('punkt') #if can't not run please remove comment in here
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk import pos_tag


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

@shared_task(name="get_data")
def getDataCelery():
    getDataProfile()
    getDataArticle()


@shared_task(name="word_cloud")
def word_cloud(userId):
    labeltitle = []
    datatitle = []
    user = User.objects.get(id = userId)
    listArticle = Article.objects.filter(user = user)
    for item in listArticle:
        text_tokens = nltk.word_tokenize(str(item.title))
        text_tokens = [word for word in text_tokens if not word in stopwords.words('english')]
        text_tokens = pos_tag(text_tokens) 
        title=[x for (x,y) in text_tokens if y not in ('PRP$', 'VBZ','POS', 'DT', 'VBD','CD', '.', ',',':', ')', '(', '}', '{', '/', '[', ']') and re.match("[a-zA-Z0-9]+",y)]
        for word in title:
            try:
                index = labeltitle.index(word.lower())
            except:
                index = None
            if index:
                datatitle[index]+=1
            else:
                labeltitle.append(word.lower())
                datatitle.append(1)
    list = [(datatitle[i], labeltitle[i]) for i in range(len(datatitle))]
    datatitle.sort()
    labeltitle = [x[1] for i in range(len(datatitle)) for x in list if x[0] == i]
    datatitle=datatitle[::-1] 
    labeltitle=labeltitle[::-1] 
    return labeltitle, datatitle

@shared_task(name="get_citations")
def get_citations(userId):
    labels = []
    data = []
    totalCitations=0
    totalCitationsSince=0
    user = User.objects.get(id = userId)
    listArticle = Article.objects.filter(user = user)
    if listArticle:
        articlelist = listArticle.order_by('-year')
        index = 0
        while not articlelist[index].year:
            index+=1
        if index==len(articlelist)-1:
            max=0
        else:
            try:
                max = int(articlelist[0].year)
            except:
                max = date.today().year
        index =len(articlelist)-1
        while not articlelist[index].year:
            index-=1
        min = 0 if index==0 else int(articlelist[index].year)
        for x in range(min, max+1):
            labels.append(x)
            cyted = 0 
            for article in articlelist:
                if article.year and x == int(article.year) and article.total_citations:
                    cyted += int(article.total_citations)
                    totalCitations+=int(article.total_citations)
                    if x>=2016:
                        totalCitationsSince+=int(article.total_citations)
            data.append(cyted)
    return labels, data, totalCitations, totalCitationsSince

     

