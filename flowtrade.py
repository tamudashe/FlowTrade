import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web  # to get data from yahoo finance api


df = pd.read_csv("apple.csv", parse_dates=True, index_col=0)

df_ohlc = df["Adj Close"].resample("10D").ohlc()
df_volume = df["Volume"].resample("10D").sum()

print(df_ohlc.head())

# reset index
df_ohlc.reset_index(inplace=True)

df_ohlc["Date"] = df_ohlc["Date"].map(mdates.date2num)

print(df_ohlc.head())

ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1)
