import pandas as pd
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs
import time
import random
import re


serum_df_test = pd.read_csv('serum_drop_duplicates.txt').head(50)

urls = serum_df_test['url']

ua = UserAgent().chrome

headers = {'User-Agent':ua}

importantInfoID = re.compile('importantInformation.*')


def get_ingredients(url):
    response = requests.get(url,headers=headers)
    html = response.text
    soup = bs(html,"lxml")
    try:
        importantInfo = soup.find(id=importantInfoID).get_text().replace('\n','')
        searchPattern = r'Ingredients(.*?)(Directions|Indications|Legal Disclaimer)'
        ingredients = re.search(searchPattern,importantInfo).group(1)
        return ingredients


    except:
        print ("{}\nNo important information div on the page.".format(url))
        return None

data = []
for url in urls:
    time.sleep(random.expovariate(10))
    ingredients = get_ingredients(url)
    data.append(ingredients)

serum_df['ingredients'] = pd.Series(data).values









