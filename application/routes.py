from application import app
from flask import render_template, request, json, jsonify
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder
import requests
import numpy
import pandas as pd

#decorator to access the app
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

#decorator to access the service
@app.route("/stock_predict", methods=['GET', 'POST'])
def stock_predict():

    #extract form inputs
    ticker_value = request.form.get("ticker")


   #convert data to json
    input_data = json.dumps({"ticker": ticker_value})

    companyname_dict = {"AAPL": "Apple", "AMZN": "Amazon", "META": "Meta"}

    #url for bank marketing model
    #url = "http://localhost:5000/api"
    url = "https://dsm-stock-model-bcb189c36199.herokuapp.com/api"
  
    #post data to url
    results =  requests.post(url, input_data)
    results_every =(pd.DataFrame.from_dict(results.json(), orient="index"))
    #results_every = pd.read_json(results.json(), orient = 'index')
    #send input values and prediction result to index.html for display
    return render_template("index.html", ticker = ticker_value,  average= results.json()['20_day_average'],
                           median = results.json()['20_day_median'], low = results.json()['20_day_low'], 
                           high = results.json()['20_day_high'],
                           company = companyname_dict[ticker_value])
    #return results