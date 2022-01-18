# -*- coding: utf-8 -*-
"""

This script is used to scrape all schools from class 5-13 in saarland.

@author: Moritz Wegener, moritz.wegener@uni-koeln.de
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup
###get all search urls###
shorts = ["bs","ers","gy","rs"]
basic_url = "https://www.saarland.de/mbk/DE/portale/bildungsserver/themen/schulen-und-bildungswege/schuldatenbank/_functions/Schulsuche_Formular.html?schulformKurzbez_str="
result_list = []
link_list = open("../data/link_liste_saarland.txt", "r")
urls = link_list.read()
url_list = urls.split(",")
link_list.close()
###iterat over all links###
for url in url_list:
    ###acces source code###
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    ###extract schools###
    school_list = soup.find_all('div',{'class':'c-searchresult-teaser__text'})
    for school in school_list:
        ###extract data###
        name = school.find('h3').decode_contents().lstrip().rstrip()
        street = school.find('p').decode_contents().split(", ")[0]
        zip_code = school.find('p').decode_contents().split(", ")[1].split(' ')[0]
        city = school.find('p').decode_contents().split(", ")[1].split(' ')[1]
        result_list.append({"name":name,"city":city,"zip_code":zip_code,"street":street})
        ###creat csv file###
        result = pd.DataFrame(result_list)  
        result.to_csv("../results/db_saarland.csv",encoding="utf-8",sep=",",index=False)