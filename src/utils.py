# -*- coding: utf-8 -*-
import pandas as pd
from pandas import Series, DataFrame, MultiIndex
import matplotlib
import numpy as np
from layout import *
idx = pd.IndexSlice

roomnames_dict={'Room_Living':'Livingroom','Room_Kitchen':'Kitchen','Room_Sleeping':'Bedroom','Room_Children':'Childrenroom','Room_Bath':'Bath'}

def delColLev(DataFrameIn, levels=[]):
        cols=DataFrameIn.columns.values
        cols=np.array(list(cols)).T
        #print cols, cols[0]
        counts=0
        for level in range(len(cols)):
            if level not in levels:
                counts+=1
                if counts==1:
                    newCols=np.array([cols[level]])
                else:
                    newCols=np.concatenate((newCols,[cols[level]]))
        DataFrameIn.columns=MultiIndex.from_arrays(newCols)
        return DataFrameIn

def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(int(100 * y))

    # The percent symbol needs escaping in latex
    if matplotlib.rcParams['text.usetex'] == True:
        return s + r'$\%$'
    else:
        return s + '%'

