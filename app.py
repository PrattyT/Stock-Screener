import os, csv
import numpy
import talib
from flask import Flask, render_template, request
from patterns import patterns
import yfinance as yf
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    pattern = request.args.get('pattern', default = None)
    stocks = {}

    with open('datasets/companies.csv') as f:
        for row in csv.reader(f) :
            stocks[row[0]] = {'company' : row[1]}


    if pattern:
        datafiles = os.listdir('datasets/daily')
        for filename in datafiles:
            df = pd.read_csv('datasets/daily/{}'.format(filename))
            pattern_function = getattr(talib, pattern)
            symbol = filename.split('.')[0]
            try:
                result = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
                last = result.tail(1).values[0]

                if last > 0:
                    stocks[symbol][pattern] = 'bullish'
                elif last < 0:
                    stocks[symbol][pattern] = 'bearish'
                else:  
                    stocks[symbol][pattern] = None
            except:
                pass

    return render_template('index.html', patterns = patterns, stocks = stocks, current_pattern = pattern)


@app.route("/snapshot")
def snapshot():
    with open('datasets/companies.csv') as f:
        companies = f.read().splitlines()
        for company in companies:
            symbol = company.split(',')[0]
            print(symbol)
            df = yf.download(symbol, start = "2021-01-01", end = "2021-05-16")
            df.to_csv('datasets/daily/{}.csv'.format(symbol))

    return { 
        'code': 'hi'
    }