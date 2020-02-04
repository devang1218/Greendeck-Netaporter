#1. NAP products where discount is greater than n%

import json
import pandas as pd

def discounted_products_list(query):
    product_json=[]
    with open('dumps/netaporter_gb_similar.json') as fp:
        for product in fp.readlines():
            product_json.append(json.loads(product))
    df=pd.read_json("dumps/netaporter_gb_similar.json",lines=True,orient='columns')

    l1=[]        
    for k in range(len(query["filters"])):
        t=[]
        if query["filters"][k]["operand1"]=="discount":
            if query["filters"][k]["operator"]==">":
                for i in range(len(df["price"])):
                    if ((df["price"][i]["regular_price"]["value"]-df["price"][i]["offer_price"]["value"])>query["filters"][k]["operand2"]):
                        if k==0:
                            l1.append(df["_id"][i]["$oid"])
                        
                        if df["_id"][i]["$oid"] in l1 and k!=0:
                            t.append(df["_id"][i]["$oid"])

            if query["filters"][k]["operator"]=="==":
                for i in range(len(df["price"])):
                    if ((df["price"][i]["regular_price"]["value"]-df["price"][i]["offer_price"]["value"])==query["filters"][k]["operand2"]):
                        if k==0:
                            l1.append(df["_id"][i]["$oid"])
                        
                        if df["_id"][i]["$oid"] in l1 and k!=0:
                            t.append(df["_id"][i]["$oid"])

            if query["filters"][k]["operator"]=="<":
                for i in range(len(df["price"])):
                    if ((df["price"][i]["regular_price"]["value"]-df["price"][i]["offer_price"]["value"])<query["filters"][k]["operand2"]):
                        if k==0:
                            l1.append(df["_id"][i]["$oid"])
                        
                        if df["_id"][i]["$oid"] in l1 and k!=0:
                            t.append(df["_id"][i]["$oid"])
            # return jsonify({"discounted_products_list":l1})

        if query["filters"][k]["operand1"]=="brand.name":
            for i in range(len(df["brand"])):
                if (df["brand"][i]["name"]==query["filters"][k]["operand2"]):
                    if k==0:
                        l1.append(df["_id"][i]["$oid"])
                        
                    if df["_id"][i]["$oid"] in l1 and k!=0:
                        t.append(df["_id"][i]["$oid"])
        
        if k!=0:
            l1 = t

    return l1