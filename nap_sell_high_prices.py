#3. NAP products where they are selling at a price higher than any of the competition.    

import json
import pandas as pd

product_json=[]
with open('dumps/netaporter_gb_similar.json') as fp:
    for product in fp.readlines():
        product_json.append(json.loads(product))
df=pd.read_json("dumps/netaporter_gb_similar.json",lines=True,orient='columns')

#website_id's other than NAP    
l = ['5da94f4e6d97010001f81d72', '5da94f270ffeca000172b12e', '5d0cc7b68a66a100014acdb0', '5da94ef80ffeca000172b12c', '5da94e940ffeca000172b12a']

def nap_sell_high_prices(query):
    nap_id=[]
    #list to input NaN so not to encounter any error in future
    p=[]
    l1 = list(df["similar_products"].isna())
    for i in range(len(l1)):
        if l1[i] ==True:
            p.append(i)

    if "filters" in query:
        for k in range(len(query["filters"])):
            if query["filters"][k]["operand1"]=="brand.name" and query["filters"][k]["operator"]=="==":
                for i in range(len(df["price"])):
                    if df["brand"][i]["name"] == query["filters"][k]["operand2"] and (i not in p) and df["similar_products"][i]["meta"]["total_results"] >0:
                        for j in l:
                            if df["similar_products"][i]["website_results"][j]["knn_items"]!=[] and df["similar_products"][i]["website_results"][j]["knn_items"][0]["_source"]["price"]["basket_price"]["value"]<df["price"][i]["basket_price"]["value"]:
                                nap_id.append(df["_id"][i]["$oid"])
                                break
    
    else:
        for i in range(len(df["price"])):
            if (i not in p) and df["similar_products"][i]["meta"]["total_results"] >0:
                for j in l:
                    if df["similar_products"][i]["website_results"][j]["knn_items"]!=[] and df["similar_products"][i]["website_results"][j]["knn_items"][0]["_source"]["price"]["basket_price"]["value"]<df["price"][i]["basket_price"]["value"]:
                        nap_id.append(df["_id"][i]["$oid"])
                        break
    return nap_id