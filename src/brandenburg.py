# -*- coding: utf-8 -*-
"""

This script is used to scrape all schools from class 5-13 in brandenburg based on the city id.

@author: Moritz Wegener, moritz.wegener@uni-koeln.de
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
###creat basic urls###
result_list = []
basic_url_part_1 = "https://schulen.brandenburg.de/suche?type=nameSearch&resultType=list&page="
basic_url_part_2 = "&showFilters=true&searchString=&filterSchulform=12&filterSchulform=22&filterSchulform=25&filterSchulform=33&filterSchulform=18&filterTraeger="
school_list = []
###we got 11 pages for our filter so iterrat over all and acces school data##
for i in range(0,12):
    ###acces source code###
    current_url = basic_url_part_1+ str(i) + basic_url_part_2
    page = requests.get(current_url).text
    soup = BeautifulSoup(page, 'html.parser')
    ###get all schools on each page and extract data###
    school_list = soup.find_all('li', class_='list-item')
    for school in school_list:
        name = school.find("h2", {"class": "schulname"}).text
        search_string = re.sub("\s\s+",' ', school.find("p").text)
        reg_ex_match = re.match("(.*) ([0-9]{5}) (.*)", search_string)
        street = reg_ex_match.group(1)
        zip_code = reg_ex_match.group(2)
        city = reg_ex_match.group(3)
        result_list.append({"name":name,"city":city,"street":street,"zip_code":zip_code})
        ###creat csv file###
        result = pd.DataFrame(result_list)  
        result.to_csv("../results/brandenburg.csv",encoding="utf-8",sep=",",index=False)