from __future__ import absolute_import, unicode_literals
from celery import shared_task
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk import pos_tag
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core import serializers
import re
from .models import Article, KeywordResearch
from django.contrib.auth.models import User
from datetime import date
from django.db.models import Q





@shared_task
def keyword_research(getTitle):
    articles = Article.objects.filter(Q(title__icontains=getTitle) | Q(author__icontains=getTitle))
    if getTitle and articles:
        title = str(articles[0]).lower()
        title = title.strip()     
        text_tokens = nltk.word_tokenize(title)
        text_tokens = [word for word in text_tokens if not word in stopwords.words('english')]
        text_tokens = pos_tag(text_tokens) 
        title=[x for (x,y) in text_tokens if y not in ('PRP$', 'VBZ','POS','DT',':',')','(','.',',')]
        if getTitle:
            keywords = str(getTitle).strip()
            text_tokens = nltk.word_tokenize(keywords)
            text_tokens = [word for word in text_tokens if not word in stopwords.words('english')]
            text_tokens = pos_tag(text_tokens) 
            keywords = [x for (x,y) in text_tokens if y not in ('PRP$', 'VBZ','POS', 'DT','.', ',',':', ')', '(', '}', '{', '/', '[', ']') and re.match("[a-zA-Z0-9]+",y) and x.lower() in title]
            for keyword in keywords:
                try:
                    keywordResearch = KeywordResearch.objects.get(keyword = keyword.lower())
                except KeywordResearch.DoesNotExist:
                    keywordResearch = None
                if keywordResearch:
                    keywordResearch.quantity += 1
                    keywordResearch.save()
                else:
                    keywordResearch = KeywordResearch(keyword = keyword.lower(), quantity = 1)
                    keywordResearch.save()
        
        