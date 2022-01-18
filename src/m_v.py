# -*- coding: utf-8 -*-
"""
This script is used to scrape all schools from class 5-13 in mecklenburg vorpommern.

@author: Moritz Wegener, moritz.wegener@uni-koeln.de
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup
###get list of all school urls###
result_list = []
link_list = open("../data/link_liste_m_v.txt", "r")
urls = link_list.read()
url_list = urls.split(",")
link_list.close()
###iterat over all links###
for url in url_list:
    ###acces source code###
    r = requests.get(url)
    page = str(requests.get(url).content.decode("utf-8") )
    soup = BeautifulSoup(page, 'html.parser')
    ###extract data###
    name = soup.find("p",{"class":'map_title'}).decode_contents()
    street = soup.find("span",{"itemprop":"streetAddress"}).decode_contents()
    zip_code = soup.find("span",{"itemprop":"postalCode"}).decode_contents()
    city = soup.find("span",{"itemprop":"addressLocality"}).decode_contents()
    result_list.append({"name":name,"city":city,"street":street,"zip_code":zip_code})
    ###creat csv file###
    result = pd.DataFrame(result_list)  
    result.to_csv("../results/db_mv.csv",encoding="utf-8",sep=",",index=False)