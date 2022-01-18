# -*- coding: utf-8 -*-
"""

This script is used to scrape all schools from class 5-13 in sachsen.

@author: Moritz Wegener, moritz.wegener@uni-koeln.de
"""
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
###get all search urls###
result_list = []
link_list = open("../data/link_liste_sachsen.txt", "r")
urls = link_list.read()
url_list = urls.split(",")
link_list.close()
basic_url = 'https://schuldatenbank.sachsen.de/'
###iterat over all links###
for url in url_list:
    ###acces source code###
    page = requests.get(basic_url+url).text
    soup = BeautifulSoup(page, 'html.parser')
    ###extract data###
    name = soup.find("p", {"class": "contact-visitor"}).find("span",{"class":"contact-content"}).decode_contents().split("<br/>")[1]
    street = soup.find("p", {"class": "contact-visitor"}).find("span",{"class":"contact-content"}).decode_contents().split("<br/>")[2]
    zip_code = soup.find("p", {"class": "contact-visitor"}).find("span",{"class":"contact-content"}).decode_contents().split("<br/>")[3].split("<br>")[0].split(' ')[0]
    city = soup.find("p", {"class": "contact-visitor"}).find("span",{"class":"contact-content"}).decode_contents().split("<br/>")[3].split("<br>")[0].split(' ')[1]
    try:
        maps_string = soup.find("p", {"class": "contact-visitor"}).find("span",{"class":"contact-content"}).decode_contents().split("<br/>")[3].split("<br>")[1]
        lat = re.search("https:\/\/www.google.de\/maps\?q=([0-9\.]*),([0-9\.]*)", maps_string).group(1)
        lon = re.search("https:\/\/www.google.de\/maps\?q=([0-9\.]*),([0-9\.]*)", maps_string).group(2)
    except Exception as e:
        lat = "no_data"
        lon = "no_data"
    result_list.append({"name":name,"city":city,"street":street,"zip_code":zip_code,'lat':lat,'lon':lon})
    ###creat csv file###
    result = pd.DataFrame(result_list)  
    result.to_csv("../results/db_sachsen.csv",encoding="utf-8",sep=",",index=False)
    