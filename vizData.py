import datetime as dt
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")


def viz_data():
    df = pd.read_csv("sp500Joined.csv")
    get_corelation = df.corr()

    data = get_corelation.values  # numpy array of columns and rows
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)

    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)

    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_label = get_corelation.columns
    row_label = get_corelation.index

    ax.set_xticklabels(column_label)
    # ax.set_ytickslabels(row_label)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1, 1)

    plt.tight_layout()
    plt.show()


viz_data()
