from pickle import GLOBAL
from tarfile import NUL
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import render

from article.models import Article
from Scholar.getDataScholar import data_scrap,data_profile
from register.models import UserProfile
from asgiref.sync import sync_to_async

import time

from urllib.parse import urlparse
import urllib.request as urllib2
from django.core.files import File
from django.core.files.base import ContentFile
import io





# Create your views here.


# import pyodbc 
    

def home(request):
    # cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-EF058DF;DATABASE=dataScholar;Trusted_Connection=yes;')

    # cursor = cnxn.cursor()
    # cursor.execute('SELECT * FROM Article')
    # i=0
    # for row in cursor:
    #     i+=1
    #     if i>=104:
    #         article = Article(user = User.objects.get(id=3), title = row[2],author=row[3], publication_date=row[4], journal=row[5], conference=row[9], total_citations= row[13])
    #         print(article)
    #         article.save()
    
    # str = 'acdefghijklmnopqrstuvwxyz'
    #    
    # for x in str:
    #     data_profile('https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors='+x)
    global profile
    if request.user.is_authenticated: 
        try:
            profile = UserProfile.objects.get(user = request.user)
        except:
            profile = None   
        # print(profile)
        if profile == None:
            profile == UserProfile(user = request.user, name = request.user.get_full_name(), Affiliation=request.user.email, EmailForVerification = 'Verified email at fpt.edu.vn').save()
            profile = UserProfile.objects.get(user = request.user)
            img_url='https://sqlvan3doctgbfyraq.blob.core.windows.net/vulnerability-assessment/media/images/avatar_scholar_56_WcEBGcd.png'
            name_image = str(request.user)
            content = io.BytesIO(urllib2.urlopen(img_url).read())
            profile.avatar.save(name_image, content, save=True)
            profile.save()
            request.session['user'] = { 'image': profile.avatar.url }
        else:
            profile = UserProfile.objects.get(user = request.user)
            request.session['user'] = { 'image': profile.avatar.url }
    return render(request, 'home/index.html')  



def handler404(request,exception):
    return render(request, '404.html', status=404)

def handler500(request, *args, **argv):
    return render(request, '500.html', status=500)