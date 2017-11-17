import pandas as pd
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs
import time
import random
import re


serum_df_test = pd.read_csv('serum_drop_duplicates.txt')

urls = serum_df_test['url']

ua = UserAgent().chrome

headers = {'User-Agent':ua}

importantInfoID = re.compile('importantInformation.*')
product_info= re.compile(r'Product Description', re.IGNORECASE|re.UNICODE)
list_in = []
def get_ingredients(url):
    response = requests.get(url,headers=headers)
    html = response.text
    soup = bs(html,"lxml")
    try:
        importantInfo = soup.find(id=importantInfoID).get_text().replace('\n','')
        searchPattern = r'Ingredients(.*?)(Directions|Indications|Legal Disclaimer)'
        ingredients = re.search(searchPattern,importantInfo)
        if ingredients:
            list_in.append(ingredients.group(1))
        else:
            return None
    except:
        try:
            product_details=soup.find(string=product_info)
            ingredient=product_details.findNext('p').get_text().replace(u'\xa0', u' ').strip()
            list_in.append(ingredient)
        except:
            print ("{}\nNo important information div on the page.".format(url))
            return None


data = []
for url in urls:
    time.sleep(random.expovariate(10))
    ingredients=get_ingredients(url)
    data.append(ingredients)

serum_df_test['ingredients'] = pd.Series(data).values
print(serum_df_test)
serum_df_test.to_csv("serum_with_ingredients.txt",index=False)


## ingredients analysis ##
# extract stop words from ingredients' info
def get_contents(url):
    response = requests.get(url, headers=headers)
    # print (url)
    html = response.text
    dict_content= bs(html,'lxml')
    return dict_content


def ingre_dict():
    item_dict={}
    url='http://www.paulaschoice.com/ingredient-dictionary'
    response= requests.get(url,headers=headers)
    dict_content= response.text
    soup=bs(dict_content,'lxml')
    items = soup.find_all('h2',"name ingredient-name")
    for i in items:
        name=i.get_text()
        name=name.strip().replace(',','-')
        i_url=i.a.get('href')
        item_contents= get_contents(i_url)
        score = re.compile(r'rating-.*')
        rating = item_contents.find('span',score).get_text()
        category = item_contents.find("div", "u-miscellaneous-pagetitle").findNext('a').get_text()
        try:
            contents = item_contents.find("div", "upper-body").p.get_text().strip().replace(u'\xa0', u' ')
        except:
            try:
                contents = item_contents.find("div", "upper-body").get_text().strip().replace(u'\xa0', u' ')
            except:
                contents = ""
        item_dict[name]={}
        item_dict[name]['url']=i_url
        item_dict[name]['functions']= contents
        item_dict[name]['rating'] = rating
        item_dict[name]['category']= category
    return (item_dict)

with open ('ingredients_dictionary.txt','w') as file:
    json.dumps(ingre_dict())

