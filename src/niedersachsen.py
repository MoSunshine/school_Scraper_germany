# -*- coding: utf-8 -*-
"""
This script is used to scrape all schools from class 5-13 in mecklenburg vorpommern based on the city id.

@author: Moritz Wegener, moritz.wegener@uni-koeln.de
"""
import requests
import pandas as pd
import json
###load url list###
result_list = []
link_list = open("../data/link_liste_niedersachsen.txt", "r")
urls = link_list.read()
url_list = urls.split(",")
link_list.close()
###creat basic urls###
basic_url = "https://schulen.nibis.de/school/getInfo/"
###iterat over all links###
for url in url_list:
    ###acces source code###
    page = requests.get(basic_url+url).text
    json_object = json.loads(page)
    ###extract data###
    name = json_object["schulname"]
    street = json_object["sdb_adressen"][0]["strasse"]
    city = json_object["sdb_adressen"][0]["sdb_ort"]["ort"]
    zip_code = json_object["sdb_adressen"][0]["sdb_ort"]["plz"]
    result_list.append({"name":name,"city":city,"street":street,"zip_code":zip_code})
    ###creat csv file###
    result = pd.DataFrame(result_list)  
    result.to_csv("../results/db_niedersachsen.csv",encoding="utf-8",sep=",",index=False)