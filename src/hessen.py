# -*- coding: utf-8 -*-
"""
This script is used to scrape all schools from class 5-13 in hessen based on the city id.

@author: Moritz Wegener, moritz.wegener@uni-koeln.de
"""
import requests
import pandas as pd
import time 
from bs4 import BeautifulSoup
###get list of all school urls###
link_list = open("../data/link_liste_hessen.txt", "r")
urls = link_list.read()
url_list = urls.split(",")
link_list.close()
result_list = []
###iterat over all links###
for link in url_list:
    ###acces source code###
    page = requests.get(link).text
    time.sleep(1)
    soup = BeautifulSoup(page, 'html.parser')
    ###extract data###
    name = soup.find("pre").text.splitlines()[1]
    street = soup.find("pre").text.splitlines()[2]
    zip_code = soup.find("pre").text.splitlines()[3].split(" ")[0]
    city = soup.find("pre").text.splitlines()[3].split(" ")[1]
    result_list.append({"name":name,"city":city,"zip_code":zip_code,"street":street})
    ###creat csv file###
    result = pd.DataFrame(result_list)  
    result.to_csv("../results/db_hessen.csv",encoding="utf-8",sep=",",index=False)
    