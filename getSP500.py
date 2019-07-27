import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests


def get_sp500_tickers():
    responce = requests.get(
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = bs.BeautifulSoup(responce.text, "lxml")
    table = soup.find("table", {"class": "wikitable sortable"})
    tickers = []
    for row in table.findAll("tr")[1:]:
        ticker = row.findAll("td")[0].text
        # Scraping from wikipedia returns 'MMM/n' to the pickle file.
        ticker = ticker[:-1]
        tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    return tickers


def get_yahoo_data(reload_sp500=False):
    if reload_sp500:
        tickers = get_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists("stock_data"):
        os.makedirs("stock_data")

    start = dt.datetime(2009, 7, 26)
    end = dt.datetime(2019, 7, 26)

    for ticker in tickers:
        if not os.path.exists("stock_data/{}.csv".format(ticker)):
            try:
                df = web.DataReader(ticker, "yahoo", start, end)
                df.to_csv("stock_data/{}.csv".format(ticker))
            except:
                print("Unable to get {}".format(ticker))
        else:
            print("Already have {}".format(ticker))
