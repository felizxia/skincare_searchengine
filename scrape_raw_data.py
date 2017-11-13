from amazon.api import AmazonAPI
import pandas as pd
import numpy as np
import random
import time


AMAZON_ACCESS_KEY= 'AKIAIBC3KZS5VDDRDKRA'
AMAZON_SECRET_KEY = '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'
AMAZON_ASSOCIATE_TAG = 'si650-20'
amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOCIATE_TAG,MaxQPS=0.7)


data = []
priceRange = np.arange(5,205,5)

def search(minPrice,maxPrice):
    # get up to 100 results per range
    products = amazon.search(Keywords='serum',
                         SearchIndex='Beauty',
                         MinimumPrice = minPrice,
                         MaximumPrice = maxPrice,
                         BrowseNode=7792528011)
    # append product to dataframe
    for i,product in enumerate(products):
        row = [product.asin,product.title, product.formatted_price, product.brand, product.features, product.detail_page_url]
        print (i)
        print (row)
        data.append(row)



def main():
    for startPrice, endPrice in zip(priceRange, priceRange[1:]):
        time.sleep(random.expovariate(1))
        search(startPrice*100, endPrice*100)
    serum_df = pd.DataFrame(data,columns=['asin','title', 'price', 'brand', 'features', 'url'])
    serum_df.to_csv("serum_2.txt",index=False)

main()





