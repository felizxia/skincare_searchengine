
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from whoosh.index import create_in
from whoosh.fields import *
import os.path
from whoosh import index
from whoosh.fields import Schema, ID, TEXT
from whoosh.analysis import StemmingAnalyzer
import pandas as pd
from whoosh.writing import AsyncWriter
# create the index from scratch

def clean_index(dirname,path):
    ix = create_in(dirname, schema=get_schema())
    writer = AsyncWriter(ix)
    # Assume we have a function that gathers the filenames of the documents to be indexed
    with writer as w:
        content = pd.read_csv(path)
        for i in range(len(content)):
            print(content.loc[i][2]) # float(str(content.loc[i][2]).replace('$',''))
            w.add_document(path=str(content.loc[i][0]), title=str(content.loc[i][1]),price=float(str(content.loc[i][2]).replace('$','')),brand=str(content.loc[i][3]), feature=str(content.loc[i][4]),url=str(content.loc[i][5]),ingre_functions= str(content.loc[i][6]),rating_content= str(content.loc[i][7]),ingredients_score = str(content.loc[i][9]), ingredients_index= str(content.loc[i][10]), feature_index= str(content.loc[i][11])) #.tolist()

def get_schema():
    return Schema(path=ID(unique=True, stored=True), title=TEXT(stored=True),feature=TEXT(stored=True,analyzer=StemmingAnalyzer()),price= NUMERIC(numtype=int,sortable=True,stored=True),brand= TEXT(stored=True),url=STORED,rating_content=STORED,ingre_functions=TEXT(stored=True,analyzer=StemmingAnalyzer()),ingredients_score=NUMERIC(numtype=int,sortable=True,stored=True),ingredients_index=TEXT(stored=True,analyzer=StemmingAnalyzer()),feature_index=TEXT(stored=True,analyzer=StemmingAnalyzer())) # ,price=TEXTfunction=KEYWORD  ; NUMERIC(float,sortable=True,stored=True)

# clean_index('test','all_serum.csv')

# open index dir
skincare = index.open_dir("test")
print(skincare.schema.names())
# care search index
from whoosh.qparser import QueryParser,MultifieldParser
from whoosh import scoring
from whoosh import columns, fields, index, sorting
from whoosh.lang.porter import stem
from whoosh.lang.morph_en import variations
from whoosh.highlight import highlight
# qp = QueryParser("function", schema=skincare.schema)
qp = MultifieldParser(fieldnames=["title","feature","feature_index","ingre_functions",'ingredients_index',"brand"],schema=skincare.schema)
qstring= u"natural moisturizer"
q = qp.parse(qstring)
# present search results of top rank or i page
with skincare.searcher(weighting=scoring.TF_IDF()) as s: # weighting model can be TF_IDF or BM25()
    corrected = s.correct_query(q, qstring)
    if corrected.query != q:
        print("Did you mean:", corrected.string + str('?'))

    else:
        # mf = sorting.MultiFacet()# mf.add_field("price")
        # mf.add_field("ingredients_score", reverse=True)
        results = s.search(q,terms=True)
        # print(q.all_terms() - results.terms())
        keywords = [keyword for keyword, score in results.key_terms("feature", docs=10, numterms=5)] ## extract keywords from field
        print(keywords)
        for hit in results:
            print(hit["title"],hit['price'],hit['url'])
            print(hit.matched_terms())
  
