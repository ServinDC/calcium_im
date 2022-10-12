#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: servindc
"""

import numpy as np
import pandas as pd
#import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def read_csv_dropcol(filename, drop_first_col=True):
    "Reads a csv file droping its first column"
    if drop_first_col==True:
        # sets first named column as the index column (drops first idx column)
        df = pd.read_csv(filename, index_col=0)
        # resets the index to begin with zero
        df.reset_index(drop=True, inplace=True)
        return df

def find_bottom_idx(x, a, b, dx_treshold=10):
    "Finds index of 'x' before maximum derivative (between indexes 'a' and 'b')"
    if a>b:
        print("find_bottom_idx(): 'a' must be smaller than 'b'.")
        return
    # derivative values
    x = x[a:b+1]
    idx_dx = np.argwhere(np.gradient(x)>dx_treshold)[0,0] -1
    return idx_dx + a

def find_all_bottoms_idx(df, dx_treshold=10):
    mins = []
    for i in range(df.shape[1]):
        x = df.iloc[:,i] #:100
        try:
            a, b = 280, 310
            idx_dx = find_bottom_idx(x, a, b, dx_treshold=dx_treshold)
        except IndexError:
            print("INFO: find_all_bottoms_dx(): IndexError\n index not found.")
            idx_dx = a
        mins.append(idx_dx)
    return mins

def find_slope_all(df, idx_1, idx_2, dx_treshold=10):
    """ Fits line between indexes and returns slope and intercept
        type(idx_1)=int, type(idx_2)=list
    """
    slopes, y_inter = [], []
    for i in range(df.shape[1]):
        x = df.iloc[:,i]
        y = x[idx_1:idx_2[i]+1]
        z = (df.index)[idx_1:idx_2[i]+1]
        a, b = np.polyfit(x=z, y=y, deg=1)
        slopes.append(a)
        y_inter.append(b)
    return slopes, y_inter

def create_csv_slopes(input_filename, idx_1, idx_2, slopes, y_inter):
    """idx_1, idx_2, slope, y-intercept
            returns name of new file
    """
    data = {'idx_1': idx_1,
                    'idx_2': idx_2,
                    'slope': slopes,
                    'y-intercept': y_inter,}
    new_df = pd.DataFrame(data)
    new_name = input_filename + "_slopes.csv"
    new_df.to_csv(new_name, index = False)
    print(f"INFO create_csv_slopes(): Created file - '{new_name}'")
    return new_name



################################################################################

if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser, RawTextHelpFormatter
    import textwrap
    #from pathlib import Path
    #from datetime import date
    
    print("")

    usage = (
        "%(prog)s datafile.csv [-h] [-i] [-o] [-d]"
        )


    sys.exit()