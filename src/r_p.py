# -*- coding: utf-8 -*-
"""

This script is used to scrape all schools from class 5-13 in reinland pfalz.

@author: Moritz Wegener, moritz.wegener@uni-koeln.de
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup
###get list of all school urls###
link_list = open("../data/link_liste_r_p.txt", "r")
urls = link_list.read()
url_list = urls.split(",")
link_list.close()
result_list = []
basic_url = "https://schulen.bildung-rp.de/"
###iterat over all links###
for link in url_list:
    url = basic_url + link
    ###acces source code###
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    ###extract data###
    name = soup.find_all('tr')[2].find('strong').decode_contents().split("<br/>")[0].replace('"','')
    street = soup.find_all('tr')[2].find('strong').decode_contents().split("<br/>")[1].replace('"','')
    zip_code = soup.find_all('tr')[2].find('strong').decode_contents().split("<br/>")[2].replace('"','').split("\xa0")[0]
    city = soup.find_all('tr')[2].find('strong').decode_contents().split("<br/>")[2].replace('"','').split("\xa0")[1]
    result_list.append({"name":name,"city":city,"zip_code":zip_code,"street":street})
    ###creat csv file###
    result = pd.DataFrame(result_list)  
    result.to_csv("../results/db_r_p.csv",encoding="utf-8",sep=",",index=False)