
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from whoosh.index import create_in
from whoosh.fields import *
import os.path
from whoosh import index
from whoosh.fields import Schema, ID, TEXT
import pandas as pd
from whoosh.writing import AsyncWriter
# create the index from scratch
# def clean_index(dirname,path):
#     ix = create_in(dirname, schema=get_schema())
#     writer = AsyncWriter(ix)
#     # Assume we have a function that gathers the filenames of the documents to be indexed
#     with writer as w:
#         content = pd.read_csv(path)
#         for i in range(1, len(content)):
#             print(content.loc[i][2])
#             w.add_document(path=str(content.loc[i][0]), title=str(content.loc[i][1]), content=str(content.loc[i][4]),price=float(str(content.loc[i][2].replace('$',''))),brand=str(content.loc[i][3]), ingre_functions= str(content.loc[i][6]),rating_content= str(content.loc[i][7]),category= str(content.loc[i][8]),ingredients_score = str(content.loc[i][9]), ingredients_index= str(content.loc[i][10]), feature_index= str(content.loc[i][10]),url=str(content.loc[i][5])) #.tolist()
#
# def get_schema():
#     return Schema(path=ID(unique=True, stored=True), title=TEXT(stored=True),content=TEXT(stored=True),price= NUMERIC(numtype=int,sortable=True,stored=True),feature=TEXT(stored=True),brand= KEYWORD(stored=True),rating=TEXT(stored=True),category=TEXT(stored=True),url=STORED) # ,price=TEXTfunction=KEYWORD  ; NUMERIC(float,sortable=True,stored=True)

# clean_index('test','all_serum_ingredients.csv')

# open index dir

skincare = index.open_dir("with_index")
print(skincare.schema.names())
# care search index
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh import columns, fields, index, sorting

# qp = QueryParser("function", schema=skincare.schema)
qp = MultifieldParser("")
q = qp.parse(u"sensitive skin japanese")


# present search results of top rank or i page
with skincare.searcher(weighting=scoring.TF_IDF()) as s: # weighting model can be TF_IDF or BM25()
    mf = sorting.MultiFacet()# mf.add_field("price")
    mf.add_field("ingredients_score", reverse=True)
    results = s.search(q,sortedby=mf)
    keywords = [keyword for keyword, score in results.key_terms("function", docs=10, numterms=5)] ## extract keywords from field
    print(keywords)
    for hit in results:
        print(hit["title"],hit['price'])
    # add sort facets

    # result_1_page= s.search_page(q, 1)