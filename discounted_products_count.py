#2. Count of NAP products from a particular brand and its average discount        

import json
import pandas as pd

def discounted_products_count(query): 
    product_json=[]
    with open('dumps/netaporter_gb_similar.json') as fp:
        for product in fp.readlines():
            product_json.append(json.loads(product))
    df=pd.read_json("dumps/netaporter_gb_similar.json",lines=True,orient='columns')

    idx =[]
    for k in range(len(query["filters"])):
        temp =[]
        if query["filters"][k]["operand1"]=="discount":
            if query["filters"][k]["operator"]==">":
                for i in range(len(df["price"])):
                    if ((df["price"][i]["regular_price"]["value"]-df["price"][i]["offer_price"]["value"])>query["filters"][k]["operand2"]):
                        if k==0:
                            idx.append(i)
                        
                        if i in idx and k!=0:
                            temp.append(i)

            if query["filters"][k]["operator"]=="==":
                for i in range(len(df["price"])):
                    if ((df["price"][i]["regular_price"]["value"]-df["price"][i]["offer_price"]["value"])==query["filters"][k]["operand2"]):
                        if k==0:
                            idx.append(i)
                        
                        if i in idx and k!=0:
                            temp.append(i)

            if query["filters"][k]["operator"]=="<":
                for i in range(len(df["price"])):
                    if ((df["price"][i]["regular_price"]["value"]-df["price"][i]["offer_price"]["value"])<query["filters"][k]["operand2"]):
                        if k==0:
                            idx.append(i)
                        
                        if i in idx and k!=0:
                            temp.append(i)
        
        if query["filters"][k]["operand1"]=="brand.name":
            for i in range(len(df["brand"])):
                if df["brand"][i]["name"]==query["filters"][k]["operand2"]:
                    if k==0:
                        idx.append(i)
                        
                    if i in idx and k!=0:
                        temp.append(i)
            
        if k!=0:
            idx = temp

    c = dis_summ = 0

    for i in idx:
        dis_summ+=(df["price"][i]["regular_price"]["value"]-df["price"][i]["offer_price"]["value"])
        c+=1

    if c!=0:
        avg_dis = dis_summ/c

    else:
        avg_dis = 0

    return c,avg_dis