# -*- coding: utf-8 -*-
"""

This script is used to scrape all schools from class 5-13 in nrw.

@author: Moritz Wegener, moritz.wegener@uni-koeln.de
"""
import requests
import pandas as pd
import time 
from bs4 import BeautifulSoup

###load html file to search###
html_search = open("../data/html_nrw_search.html", "r")
soup = BeautifulSoup(html_search, 'html.parser')
school_list = soup.find_all(attrs={"title":"Weitere Informationen - Link oeffnet ein neues Fenster"})
###creat basic url###
basic_url = "https://www.schulministerium.nrw.de/BiPo/SchuleSuchen/pages/schulsuche/"
link_list = []
result_list = []
###get all links from html doc###
for link in school_list:
    if link["href"] not in link_list:
        link_list.append(link["href"])
    else:
        pass
###iterat over all links###
for link in link_list:
    url = basic_url + link
    ###acces source code###
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    elements = soup.find_all('tr')
    ###extract data###
    name = elements[2].text.replace('\n', '').replace('\r', '').rstrip()
    street = elements[6].text.replace('\n', '').replace('\r', '').rstrip()
    city = elements[7].text.split(' ')[1].replace('\n', '').replace('\r', '').rstrip()
    zip_code = elements[7].text.split(' ')[0].replace('\n', '').replace('\r', '').rstrip()
    result_list.append({"name":name,"city":city,"street":street,"zip_code":zip_code})
    ###creat csv file###
    result = pd.DataFrame(result_list)  
    result.to_csv("../results/db_nrw.csv",encoding="utf-8",sep=",",index=False)
    