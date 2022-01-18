# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 15:19:01 2022

This script is used to scrape all schools from class 5-13 in berlin based on the city id.

@author: Moritz Wegener, moritz.wegener@uni-koeln.de
"""

import requests
import pandas as pd
import time 
from bs4 import BeautifulSoup

###creat general ulr and list of specific urls per school###
general_url = "https://www.bildung.berlin.de/Schulverzeichnis/"
link_list = open("../data/link_liste_berlin.txt", "r")
urls = link_list.read()
url_list = urls.split(",")
link_list.close()
result_list = []
###iterat over all schools###
for link in url_list:
    ###acces source code###
    url = general_url + link
    page = requests.get(url).text
    time.sleep(1)
    ###extract data and creat a csv file###
    soup = BeautifulSoup(page, 'html.parser')
    name = soup.find("span", {"id": "ContentPlaceHolderMenuListe_lblSchulname"}).text
    street = soup.find("span", {"id": "ContentPlaceHolderMenuListe_lblStrasse"}).text
    zip_code = str(soup.find("span", {"id": "ContentPlaceHolderMenuListe_lblOrt"}).text.split(" ")[0])
    city = soup.find("span", {"id": "ContentPlaceHolderMenuListe_lblOrt"}).text.split(" ")[1]
    school_id = name + "_" + street + "_" + zip_code + "_" + city
    result_list.append({"school_id":school_id,"name":name,"city":city,"zip_code":zip_code,"street":street})
    result = pd.DataFrame(result_list)  
    result.to_csv("../results/berlin.csv",encoding="utf-8",sep=",",index=False)
