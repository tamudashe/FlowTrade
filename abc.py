import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")


def viz_data():
    df = pd.read_csv("sp500JoinedCloses.csv")
    df["AAPL"].plot()
    plt.show()


viz_data()
