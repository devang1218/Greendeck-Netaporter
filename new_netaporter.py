from flask import Flask,jsonify,request
import json
import os

from discounted_products_list import discounted_products_list
from discounted_products_count import discounted_products_count
from nap_sell_high_prices import nap_sell_high_prices
from nap_sell_n_high_x import nap_sell_n_high_x


#Creating Flask Application
app = Flask(__name__)
       
@app.route("/",methods = ["GET"])
def get_function():
    return("Hello World")

@app.route("/netaporter",methods = ["POST"])
def post_function():
    query = request.get_json()

#1. NAP products where discount is greater than n%
    if query["query_type"]=="discounted_products_list":
        l1 = discounted_products_list(query)
        return jsonify({"discounted_products_list":l1})

#2. Count of NAP products from a particular brand and its average discount        
    if query["query_type"]=="discounted_products_count|avg_discount":
        c,avg_dis = discounted_products_count(query)
        return jsonify({"discounted_products_count":c,"avg_dicount":avg_dis})

#3. NAP products where they are selling at a price higher than any of the competition.    
    if query["query_type"]=="expensive_list":
        nap_id = nap_sell_high_prices(query)
        return jsonify({'expensive_list':nap_id})

#4. NAP products where they are selling at a price n% higher than a competitor X.
    if query["query_type"]=="competition_discount_diff_list":
        nap_id = nap_sell_n_high_x(query)
        return jsonify({"competition_discount_diff_list":nap_id})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)