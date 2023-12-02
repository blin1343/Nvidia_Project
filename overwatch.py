import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import re
import itertools 

urls = ["https://overwatch.blizzard.com/en-us/career/takaharimi-1252/",
       "https://overwatch.blizzard.com/en-us/career/blin1343-1104/"
       ]

data_list = []

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    num = range(1,40)

    for n in num:
        data = soup.find("span", class_ = f"stats-container option-{n}")
        heroes = soup.find("option", {"value": n})
        for d in data:
            metric = d.find_all("p", class_="name")
            value = d.find_all("p", class_="value")
            if 'Average' in d.find('p'):
                for m, v in zip(metric,value):
                    #print(n,m.text,v.text)
                    data_list.append({
                        "url": url,
                        "hero": heroes.text,
                        "hero_id": n,
                        "metric": m.text,
                        "value": v.text
                    })
                
# Create DataFrame
ow_data = pd.DataFrame(data_list)
ow_data["url"] = ow_data["url"].str.split("/").str[-2]
ow_data = ow_data[~ow_data["value"].str.contains(":")]
ow_data.astype({'value': 'float'})