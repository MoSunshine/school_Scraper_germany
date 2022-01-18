# -*- coding: utf-8 -*-
"""

This script is used to scrape all schools from class 5-13 in thüringen.

@author: Moritz Wegener, moritz.wegener@uni-koeln.de
"""
import requests
import pandas as pd
import time
import re
from bs4 import BeautifulSoup
###get all school urls###
result_list = []
link_list = open("../data/link_liste_thueringen.txt", "r")
urls = link_list.read()
url_list = urls.split(",")
link_list.close()
basic_url = "https://www.schulportal-thueringen.de/"
###iterat over all urls###
for url in url_list:
    ###acces source code###
    page = requests.get(basic_url + url).text
    soup = BeautifulSoup(page, 'html.parser')
    ###extract data###
    name = soup.find("div",{"class":"tispo_la_bigger"}).decode_contents().lstrip().rstrip()
    attr_string = soup.find("div",{"style":"padding-top: 12px;"}).decode_contents()
    street = attr_string.split("<br/>")[0].lstrip()
    zip_code = attr_string.split("<br/>")[1].lstrip().rstrip().split(" ")[0]
    city = attr_string.split("<br/>")[1].lstrip().rstrip().split(" ")[1]
    result_list.append({"name":name,"city":city,"street":street,"zip_code":zip_code})
    ###creat csv file###
    result = pd.DataFrame(result_list)  
    result.to_csv("../results/db_thueringen.csv",encoding="utf-8",sep=",",index=False)