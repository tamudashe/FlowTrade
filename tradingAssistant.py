import numpy as np
import pandas as pd
import pickle
from collections import Counter

from sklearn import svm, neighbors
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier, RandomForestClassifier


def processLabes(ticker):
    num_days = 14
    df = pd.read_csv("sp500Joined.csv", index_col=0)
    tickers = df.columns.values.tolist()
    df.fillna(0, inplace=True)

    for i in range(1, num_days + 1):
        df["{}_{}d".format(ticker, i)] = (
            df[ticker].shift(-i) - df[ticker] / df[ticker])

    df.fillna(0, inplace=True)
    return tickers, df


def tradeAssist(*args):
    columns = [col for col in args]
    benchmark = 0.05
    for col in columns:
        if col > benchmark:
            return 1
        elif col < -benchmark:
            return -1
    return 0


def get_fSets(ticker):
    tickers, df = processLabes(ticker)

    df["{}_target".format(ticker)] = list(map(tradeAssist, df["{}_1d".format(ticker)],
                                              df["{}_2d".format(ticker)],
                                              df["{}_3d".format(ticker)],
                                              df["{}_4d".format(ticker)],
                                              df["{}_5d".format(ticker)],
                                              df["{}_6d".format(ticker)],
                                              df["{}_7d".format(ticker)],
                                              df["{}_8d".format(ticker)],
                                              df["{}_9d".format(ticker)],
                                              df["{}_10d".format(ticker)],
                                              df["{}_11d".format(ticker)],
                                              df["{}_12d".format(ticker)],
                                              df["{}_13d".format(ticker)],
                                              df["{}_14d".format(ticker)],
                                              ))

    vals = df["{}_target".format(ticker)].values.tolist()
    string_vals = [str(i) for i in vals]

    print("Data spread: ", Counter(string_vals))

    df.fillna(0, inplace=True)

    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)

    df_values = df[[ticker for ticke in tickers]].pct_change()
    df_values = df_values.replace([np.inf, -np.inf], 0)
    df_values.fillna(0, inplace=True)

    X = df_values.values
    y = df["{}_target".format(ticker)].values

    return X, y, df


def machineL(ticker):
    X, y, df = get_fSets(ticker)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

    # clf = neighbors.KNeighborsClassifier()
    clf = VotingClassifier([("lsvc", svm.LinearSVC()),
                            ("knn", neighbors.KNeighborsClassifier()),
                            ("rfor", RandomForestClassifier())
                            ])

    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    print("Accouracy confidence: ", confidence)
    predictions = clf.predict(X_test)
    print("Predicted spread: ", Counter(predictions))

    return confidence


machineL("AAPL")
