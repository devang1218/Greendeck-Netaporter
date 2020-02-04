#4. NAP products where they are selling at a price n% higher than a competitor X.

import json
import pandas as pd

def nap_sell_n_high_x(query): 
    
    product_json=[]
    with open('dumps/netaporter_gb_similar.json') as fp:
        for product in fp.readlines():
            product_json.append(json.loads(product))
    df=pd.read_json("dumps/netaporter_gb_similar.json",lines=True,orient='columns')

    #list to input NaN so not to encounter any error in future
    p=[]
    l1 = list(df["similar_products"].isna())
    for i in range(len(l1)):
        if l1[i] ==True:
            p.append(i)
    nap_id = []
    opr = query["filters"][0]["operand2"]
    opr2 = query["filters"][1]["operand2"]
    if query["filters"][0]["operator"]==">":
        for i in range(len(df["price"])):
            if (i not in p) and df["similar_products"][i]["website_results"][opr2]["knn_items"]!=[]:
                comp_basket_price = df["similar_products"][i]["website_results"][opr2]["knn_items"][0]["_source"]["price"]["basket_price"]["value"]
                if (((comp_basket_price*opr)/100)+comp_basket_price) < df["price"][i]["basket_price"]["value"] :
                    nap_id.append(df["_id"][i]["$oid"])

    if query["filters"][0]["operator"]=="==":
        for i in range(len(df["price"])):
            if (i not in p) and df["similar_products"][i]["website_results"][opr2]["knn_items"]!=[]:
                comp_basket_price = df["similar_products"][i]["website_results"][opr2]["knn_items"][0]["_source"]["price"]["basket_price"]["value"]
                if (((comp_basket_price*opr)/100)+comp_basket_price) == df["price"][i]["basket_price"]["value"] :
                    nap_id.append(df["_id"][i]["$oid"])

    if query["filters"][0]["operator"]=="<":
        for i in range(len(df["price"])):
            if (i not in p) and df["similar_products"][i]["website_results"][opr2]["knn_items"]!=[]:
                comp_basket_price = df["similar_products"][i]["website_results"][opr2]["knn_items"][0]["_source"]["price"]["basket_price"]["value"]
                if (((comp_basket_price*opr)/100)+comp_basket_price) > df["price"][i]["basket_price"]["value"] :
                    nap_id.append(df["_id"][i]["$oid"])
    return nap_id
