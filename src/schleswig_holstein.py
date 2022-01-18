# -*- coding: utf-8 -*-
"""
This script is used to scrape all schools from class 5-13 in schleswig holstein.

@author: Moritz Wegener, moritz.wegener@uni-koeln.de
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
###get list of all school urls###
result_list = []
link_list = open("../data/link_liste_s_w_h.txt", "r")
urls = link_list.read()
url_list = urls.split(",")
link_list.close()
basic_url = "https://www.secure-lernnetz.de/schuldatenbank/index.php"
###iterat over all links###
for url in url_list:
    ###acces source code###
    page = requests.get(basic_url + url).text
    soup = BeautifulSoup(page, 'html.parser')
    ###extract data###
    attr_list = soup.find("form",{"id":"form_schulen_edit"}).find('tbody').find_all('tr')
    name = soup.find("form",{"id":"form_schulen_edit"}).find('thead').find_all('th')[0].decode_contents().lstrip().rstrip()
    school_id = attr_list[0].find("label",{"accesskey":"P"}).decode_contents().lstrip().rstrip()
    street = attr_list[4].find("label",{"accesskey":"P"}).decode_contents().lstrip().rstrip()
    zip_code = attr_list[5].find("label",{"accesskey":"P"}).decode_contents().lstrip().rstrip()
    city = attr_list[6].find("label",{"accesskey":"P"}).decode_contents().lstrip().rstrip()
    result_list.append({"school_id":school_id,"name":name,"city":city,"street":street,"zip_code":zip_code})
    ###creat csv file###
    result = pd.DataFrame(result_list)  
    result.to_csv("../results/db_s_w_h.csv",encoding="utf-8",sep=",",index=False)