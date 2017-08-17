import requests
from xml.etree import ElementTree as ET
import pandas as pd
import numpy as np

def nanchecker(value):
    try:
        out = np.isnan(value)
    except TypeError:
        out = False
    return out

def expand_category(df,variable):
    rowlist = df[variable].tolist()
    temp = df[variable].dropna().tolist()
    temp2 = pd.Series([item for row in temp for item in row])
    categories = temp2.unique()
    dummies = pd.DataFrame()
    for row in rowlist:
        rowdata = {}
        if nanchecker(row):
            for category in categories:
                rowdata[category] = 0
        else:
            for category in categories:
                if category in row:
                    rowdata[category] = 1
                else:
                    rowdata[category] = 0
        dummies = dummies.append(rowdata, ignore_index = True)
    return dummies

