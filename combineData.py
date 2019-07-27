import datetime as dt
import os
import pandas as pd
import pickle


def compile_data():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()  # empty dataframe
    for count, ticker in enumerate(tickers):
        if os.path.exists("stock_data/{}.csv".format(ticker)):
            print(count, ":", ticker)
            df = pd.read_csv("stock_data/{}.csv".format(ticker))
            df.set_index("Date", inplace=True)
            df.rename(columns={"Adj Close": ticker}, inplace=True)
            df.drop(["Open", "High", "Low", "Close", "Volume"], 1, inplace=True)

            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df, how="outer")

            if (count % 10) == 0:
                print(count)

    print(main_df.head())
    main_df.to_csv("sp500Joined.csv")
