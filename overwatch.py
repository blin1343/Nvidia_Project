import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
#import itertools 

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
            # Scrape all data in the Averages table
            if 'Average' in d.find('p'):
                for m, v in zip(metric,value):
                    data_list.append({
                        "url": url,
                        "hero": heroes.text,
                        "hero_id": n,
                        "metric": m.text,
                        "value": v.text
                    })
                
# Converts scraped data as a dataframe
ow_data = pd.DataFrame(data_list) 
# Extracts the unique blizzard profile from the url
ow_data["url"] = ow_data["url"].str.split("/").str[-2]

# Filter for metrics most attributable to good performance
ow_data = ow_data[ow_data["metric"].isin(["All Damage Done - Avg per 10 Min",
                                          "Hero Damage Done - Avg per 10 Min",
                                          "Eliminations - Avg per 10 Min",
                                          "Final Blows - Avg per 10 Min",
                                          "Deaths - Avg per 10 Min",
                                          "Healing Done - Avg per 10 Min"])]

# Converts value to a float
ow_data['value'] = ow_data['value'].apply(lambda x: float(x.replace(',', '')))


# Adds a new column for the role a character falls into. (could not get this data from th career profile apge)
def get_overwatch_role(character):
    overwatch_roles = {
        'Tracer': 'DPS',
        'Reaper': 'DPS',
        'Widowmaker': 'DPS',
        'Pharah': 'DPS',
        'Genji': 'DPS',
        'Cassidy': 'DPS',
        'Soldier: 76': 'DPS',
        'Sombra': 'DPS',
        'Bastion': 'DPS',
        'Hanzo': 'DPS',
        'Junkrat': 'DPS',
        'Mei': 'DPS',
        'Torbjörn': 'DPS',
        'Sojourn': 'DPS',
        'Symmetra': 'DPS',
        'Ashe': 'DPS',
        'Echo': 'DPS',
        'Bob': 'Tank',
        'D.Va': 'Tank',
        'Orisa': 'Tank',
        'Doomfist': 'Tank',
        'Reinhardt': 'Tank',
        'Roadhog': 'Tank',
        'Sigma': 'Tank',
        'Winston': 'Tank',
        'Zarya': 'Tank',
        'Junker Queen':'Tank',
        'Ramattra':'Tank',
        'Wrecking Ball':'Tank',
        'Mauga':'Tank',
        'Ana': 'Support',
        'Baptiste': 'Support',
        'Brigitte': 'Support',
        'Lúcio': 'Support',
        'Mercy': 'Support',
        'Moira': 'Support',
        'Zenyatta': 'Support',
        'Kiriko': 'Support',
        'Lifeweaver': 'Support',
        'Illari': 'Support',
    }
    # Return the role for the given character
    return overwatch_roles.get(character, 'Unknown')

ow_data["role"] = ow_data["hero"].apply(get_overwatch_role)

# Reorder the columns
ow_data = ow_data[['hero_id','hero','role','url','metric','value']]