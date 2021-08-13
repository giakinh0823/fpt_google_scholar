import re
from article.models import Article
from django.contrib.auth.models import User
from datetime import date

import nltk
nltk.download('stopwords') #if can't not run please remove comment in here
nltk.download('punkt') #if can't not run please remove comment in here
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk import pos_tag


def word_cloud(userId):
    labeltitle = []
    datatitle = []
    user = User.objects.get(id = userId)
    listArticle = Article.objects.filter(user = user)
    for item in listArticle:
        text_tokens = nltk.word_tokenize(str(item.title))
        text_tokens = [word for word in text_tokens if not word in stopwords.words('english')]
        text_tokens = pos_tag(text_tokens) 
        title=[x for (x,y) in text_tokens if y not in ('PRP$', 'VBZ','POS', 'DT', 'VBD','CD', '.', ',',':', ')', '(', '}', '{', '/', '[', ']') and bool(re.match("[a-zA-Z0-9]+",y)) and bool(re.match("[a-zA-Z0-9]+",x))]
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
    print(labeltitle)
    return labeltitle, datatitle


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