import time
import os
from pandas.core.tools.datetimes import to_datetime
import pip
import warnings
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from django.template.defaultfilters import slugify


# ignore future warnings
warnings.filterwarnings("ignore")


# call for pip command
def install(package):
    pip.main(['install', package])


# pandas, bs4, selenium, webdriver-manager, ftfy packages
def requirements_check(package):
    try:
        __import__("pandas")
        __import__("bs4")
        __import__("selenium")
        __import__("webdriver_manager")
        __import__("ftfy")
        __import__("numpy")
    except:
        import sys
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', "pandas"])
        __import__("pandas")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', "bs4"])
        __import__("bs4")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', "selenium"])
        __import__("selenium")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', "webdriver-manager"])
        __import__("webdriver_manager")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', "ftfy"])
        __import__("ftfy")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', "numpy"])


requirements_check("pandas")
requirements_check("bs4")
requirements_check("selenium")
requirements_check("webdriver_manager")
requirements_check("ftfy")
requirements_check("numpy")

# Import packages
import pandas as pd
from selenium import webdriver
from bs4 import SoupStrainer
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from ftfy import fix_encoding
import numpy as np
from webdriver_manager.utils import ChromeType

from urllib.parse import urlparse
import urllib.request as urllib2
from django.core.files import File
from django.core.files.base import ContentFile
import io
from selenium.webdriver.common.keys import Keys



from article.models import Article
from register.models import UserProfile
from django.contrib.auth.models import User

import random
import string

from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def data_profile(link):
    list_of_link =[]
    list_of_name = []
    list_of_avatar = []
    list_of_Affiliation = []
    list_of_EmailForVerification = []

    driver = webdriver.Remote("http://selenium-hub:4444/wd/hub", DesiredCapabilities.FIREFOX)
    driver.get(str(link))

    while True:
        time.sleep(2)
        htmlSource = driver.page_source
        only_id = SoupStrainer(id="gsc_sa_ccl")
        soup = BeautifulSoup(htmlSource, "html.parser", parse_only=only_id)
        
        for tr in soup.findAll("div", {"class": "gsc_1usr"}):
            for name in tr.findAll("h3", {"class": "gs_ai_name"}):
                list_of_name.append(name.find("a").text)
                if 'https://scholar' in str(name.find("a",  attrs={"href": True}).get('href')):
                    list_of_link.append(str(name.find("a",  attrs={"href": True}).get('href')))
                else:
                    list_of_link.append('https://scholar.google.com'+str(name.find("a",  attrs={"href": True}).get('href')))
            for avatar in tr.findAll("span", {"class": "gs_rimg gs_pp_sm"}):
                if 'https://scholar' in str(avatar.find("img", attrs={"src": True}).get("src")):
                    avatarMediumImage = str(avatar.find("img", attrs={"src": True}).get("src"))
                    avatarMediumImage = avatarMediumImage.replace("small_photo","medium_photo")
                    print(avatarMediumImage)
                    list_of_avatar.append(avatarMediumImage)
                else:
                    avatarMediumImage = str(avatar.find("img", attrs={"src": True}).get("src"))
                    avatarMediumImage= avatarMediumImage.replace("small_photo","medium_photo")
                    list_of_avatar.append('https://scholar.googleusercontent.com' + avatarMediumImage)
            for affiliation in tr.findAll("div", {"class": "gs_ai_aff"}):
                list_of_Affiliation.append(affiliation.text)
            for email in tr.findAll("div", {"class": "gs_ai_eml"}):
                list_of_EmailForVerification.append(email.text)
                
        
        for index in range(0,len(list_of_link)):
            try:
                profile = UserProfile.objects.get(name=fix_encoding(list_of_name[index]),Affiliation =fix_encoding(list_of_Affiliation[index]),EmailForVerification = fix_encoding(list_of_EmailForVerification[index]), homepage = list_of_link[index])
            except:
                profile = None
            # print(profile)
            if profile == None and "FPT University" in list_of_Affiliation[index] :
                # print("Set data")
                try:
                    user = User.objects.create(username = slugify(fix_encoding(list_of_link[index]).replace("https://scholar.google.com/citations?hl=en&user=", "")), password="123456")
                except:
                    user = User.objects.create(username = slugify(fix_encoding(list_of_link[index]+f"{get_random_string(2)}")), password="123456")
                user.save()
                profile = UserProfile(user = user ,name=fix_encoding(list_of_name[index]),Affiliation =fix_encoding(list_of_Affiliation[index]),EmailForVerification = fix_encoding(list_of_EmailForVerification[index]), homepage = list_of_link[index])
                img_url = list_of_avatar[index]
                name_image = urlparse(img_url).path.split('/')[-1]
                content = io.BytesIO(urllib2.urlopen(img_url).read())
                profile.avatar.save(name_image, content, save=True)
                profile.save()
        list_of_link =[]
        list_of_name = []
        list_of_avatar = []
        list_of_Affiliation = []
        list_of_EmailForVerification = []
        try:
            next_ = driver.find_element_by_xpath('//button[@aria-label="Next"]')
        except:
            next_ = None
        if next_ == None:
            break
        if next_.is_enabled() is not False:
            next_.click()
            time.sleep(6)
        else:
            break
            
    driver.close()

def data_scrap(link,userId):
    # Empty lists for storing information
    user = User.objects.get(id = userId)
    list_of_authors = []
    list_of_citation = []
    list_of_year = []
    list_of_articles = []
    list_of_journals = []
    list_of_conferences = []
    list_of_publication_date = []
    list_of_publisher = []
    list_of_pages = []
    list_of_volume = []
    list_of_issue = []
    list_of_book = []
    list_of_description = []
    list_of_pdf = []

    # Driver
    global driver    
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    driver = webdriver.Remote("http://selenium-hub:4444/wd/hub", DesiredCapabilities.FIREFOX)
    driver.get(str(link))
    time.sleep(1)
    # Locating the Show more button
    
    show_more_button = driver.find_element_by_xpath('//*[@id="gsc_bpf_more"]')
    while show_more_button.is_enabled() is not False:
        show_more_button.click()
        time.sleep(4)

    # Get author name, article name, year, total citation
    htmlSource = driver.page_source
    only_id = SoupStrainer(id="gsc_a_b")
    author_id = SoupStrainer(id="gsc_prf_in")
    soup = BeautifulSoup(htmlSource, "html.parser", parse_only=only_id)
    soup1 = BeautifulSoup(htmlSource, "html.parser", parse_only=author_id)
    author_name = soup1.find("div", {"id": "gsc_prf_in"})
    print("Author: " + author_name.text)
    for tr in soup.findAll("tr", {"class": "gsc_a_tr"}):
        for citation in tr.findAll("a", {"class": "gsc_a_ac gs_ibl"}):
            list_of_citation.append(citation.text)
        for year in tr.findAll("span", {"class": "gsc_a_h gsc_a_hc gs_ibl"}):
            list_of_year.append(year.text)
        for article in tr.findAll("a", {"class": "gsc_a_at"}):
            list_of_articles.append(article.text)
    time.sleep(2)

    link_of_button= SoupStrainer(id="gsc_a_b")
    soup_link_button = BeautifulSoup(htmlSource, "html.parser", parse_only=link_of_button)
    pdf_click_button = filter(lambda item: str(item.get("href")).find("view_op=view_citation") !=-1 ,soup_link_button.findAll("a", attrs={"href": True}))
    list_link = map(lambda item: "https://scholar.google.com"+str(item.get("href")).replace("https://scholar.google.com",""),pdf_click_button)
    index = 0

    index = 0
    
    for button in list_link:
        try:
            driver.get(button)
        except:
            continue
        time.sleep(3)

        htmlSource = driver.page_source
        only_tags_with_id = SoupStrainer(id="gs_top")
        soup = BeautifulSoup(htmlSource, "html.parser", parse_only=only_tags_with_id)
        try:
            authors = soup.findAll("div", {"class": "gsc_oci_value"})[0].text
        except:
            authors = ""
        list_of_authors.append(authors)

        link_of_pdf = SoupStrainer(id="gsc_oci_title_wrapper")
        soup_link = BeautifulSoup(htmlSource, "html.parser", parse_only=link_of_pdf)
        try:
            pdf_click = soup_link.find("a", attrs={"href": True})
            list_of_pdf.append(str(pdf_click.get('href')))
        except AttributeError:
            pdf_click = ""
            list_of_pdf.append(pdf_click)
        try:
            journal = soup.find(text="Journal").find_next().text
            list_of_journals.append(journal)
        except AttributeError:
            journal = ""
            list_of_journals.append(journal)
        try:
            conference = soup.find(text="Conference").find_next().text
            list_of_conferences.append(conference)
        except AttributeError:
            conference = ""
            list_of_conferences.append(conference)
        try:
            publication_date = soup.find(text="Publication date").find_next().text
            list_of_publication_date.append(publication_date)
        except AttributeError:
            publication_date = ""
            list_of_publication_date.append(publication_date)
        try:
            publisher = soup.find(text="Publisher").find_next().text
            list_of_publisher.append(publisher)
        except AttributeError:
            publisher = ""
            list_of_publisher.append(publisher)
        try:
            page = soup.find(text="Pages").find_next().text
            list_of_pages.append(page)
        except AttributeError:
            page = ""
            list_of_pages.append(page)
        try:
            volume = soup.find(text="Volume").find_next().text
            list_of_volume.append(volume)
        except AttributeError:
            volume = 0
            list_of_volume.append(volume)
        try:
            issue = soup.find(text="Issue").find_next().text
            list_of_issue.append(issue)
        except AttributeError:
            issue = ""
            list_of_issue.append(issue)
        try:
            book = soup.find(text="Book").find_next().text
            list_of_book.append(book)
        except AttributeError:
            book = ""
            list_of_book.append(book)
        try:
            description = soup.find(text="Description").find_next().text
            list_of_description.append(description)
        except AttributeError:
            description = ""
            list_of_description.append(description)
            
        if publication_date == "":
            Time=None
        else:
            Time = str(publication_date).replace('/','-');
        print(Time)
        if volume==0:
            volume==None
        
        try:
            getyear = list_of_year[index]
        except :
            getyear=""
        if getyear == "":
            getyear=None
        try:
            totle_citation = list_of_citation[index]
        except:
            totle_citation=""
        if totle_citation=="":
           totle_citation=None 
        try:
            newarticle = Article.objects.get(user = user, 
                             title = fix_encoding(list_of_articles[index]), 
                             author=fix_encoding(list_of_authors[index]))
        except:
            newarticle=None
        if newarticle==None:
            newarticle = Article(user = user, 
                             title = fix_encoding(list_of_articles[index]), 
                             author=fix_encoding(list_of_authors[index]), 
                             publication_date= Time,
                             journal=fix_encoding(journal),
                             book=fix_encoding(book),
                             volume=volume,
                             issue= fix_encoding(issue),
                             conference=fix_encoding(conference),
                             page=page,
                             publisher=fix_encoding(publisher),
                             description=fix_encoding(description),
                             total_citations=totle_citation,
                             year=getyear,
                             url=list_of_pdf[index],)
            newarticle.save()
            print(newarticle)
        index+=1
    driver.quit()
    print("-----------------------------------------------")
    print("Your file is ready! Check " + author_name.text)
    print("-----------------------------------------------")
    print("PROCESS ENDED.")

if __name__ == "__main__":
    data_scrap()