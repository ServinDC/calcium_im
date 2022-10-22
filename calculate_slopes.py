#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: servindc
"""

import numpy as np
import pandas as pd
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
    return pd.read_csv(filename)

def find_slope_all(df, idx_1, idx_2):
    """ Fits line between indexes and returns slope and intercept
        type(idx_1)=int or type(idx_1)=array
    """
    slopes, y_inter = [], []
    if type(idx_1) != int:                  # if idx_1 is an array
        for i in range(len(df.columns)):
            x = df.iloc[:,i]
            y = x[idx_1[i]:idx_2[i]+1]
            z = (df.index)[idx_1[i]:idx_2[i]+1]
            a, b = np.polyfit(x=z, y=y, deg=1)
            slopes.append(a)
            y_inter.append(b)
    else:                                   # if idx_1 is an int
        for i in range(len(df.columns)):
            x = df.iloc[:,i]
            y = x[idx_1:idx_2+1]
            z = (df.index)[idx_1:idx_2+1]
            a, b = np.polyfit(x=z, y=y, deg=1)
            slopes.append(a)
            y_inter.append(b)
    return slopes, y_inter

def create_csv_slopes(input_filename, idx_1, idx_2, slopes, y_inter):
    """idx_1, idx_2, slope, y-intercept
            returns name of new file
    """
    data = {'idx1': idx_1,
            'idx2': idx_2,
            'slope': slopes,
            'y-intercept': y_inter,}
    new_df = pd.DataFrame(data)
    new_name = input_filename + "_slopes.csv"
    new_df.to_csv(new_name, index = False)
    print(f"INFO create_csv_slopes(): Created file - '{new_name}'")
    return new_name

def plotly_df_slopes(df, csvfile, title=""):
    "Plots a dataframe with the slopes calculated, multiple subplots"
    n = len(df.columns)
    n_cols = 4
    n_rows = n//n_cols + bool(n%n_cols) # +1 row if n%cols not zero
    df_slopes = pd.read_csv(csvfile)

    fig = make_subplots(rows=n_rows, cols=n_cols,
                        subplot_titles=[name for name in df.columns],
                        shared_yaxes=True,# rows x cols size necessary to use h_spacing
                        specs = [[{} for i in range(n_cols)] for j in range(n_rows)],
                        horizontal_spacing = 0.02, vertical_spacing = 0.03)
    # plot dataframe columns:
    for i in range(n):
        try:
            z = df.iloc[:,i]
            s, m, a, b = df_slopes.iloc[i,:] # spike, min, ax+b
            line = z[int(s):int(m)]
            def f(x): return (a)*x+b
            fig.add_trace(go.Scatter(x=df.index, y=z,
                                     line=dict(color="#0069b9"), ),
                          row=i//n_cols+1, col=i%n_cols+1 )
            # linear fit
            z = f(line.index)
            w = line.index
            fig.add_trace(go.Scatter(x=w, y=z, line=dict(color="#cc0000"), ),
                        row=i//n_cols+1, col=i%n_cols+1,
                        )
            
            fig.add_annotation(dict(x=w[2*len(w)//3], y=z[0],
                                    text=f"m = {a:.2f}", showarrow=False),
                                    font = dict(color='#cc0000', size=14),
                                    row=i//n_cols+1, col=i%n_cols+1,)
        except:
            print(f"ERROR plotly_df_slopes(): while adding trace number {i}")
    fig.update_layout(title_text="<b>"+title+"</b>", showlegend=False,
                    height=350*n_rows, width=350*n_cols, # 5*n_cols, 4*n_rows
                    margin=dict(l=20, r=20, t=80, b=20),
                    ) # yaxis_range=[y_min-100,y_max+100],
    return fig

################################################################################

if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser, RawTextHelpFormatter
    import textwrap
    #from pathlib import Path
    #from datetime import date
    
    print("")
    script = f"{__file__.split('/')[-1]}"
    
    usage = ("%(prog)s datafile.csv [-h] [-i] [-o] [-d]")
    
    description = """
    Calculates slope between indexes, for each column of the given datafile and
    plots it; the title graph is the input filename.
    Creates two new files:
        "*_slopes.html" - file with interactive plots.
        "*_slopes.csv" - file with slope & y-intercept values.
        """

    parser = ArgumentParser(formatter_class=RawTextHelpFormatter,
        description=textwrap.dedent(description), usage=usage)
    
    parser.add_argument('datafile', type=str,
                        help="Data file (csv format).")
    parser.add_argument('-i', '--indexes', type=str, default='', metavar='',
                        help="""File with idx_1 & idx_2 of each column (csv format).\
                            \n or index pair separated by a comma (eg. "8,15").""")
    parser.add_argument('-o', '--out_prefix', default='', metavar='',
                        help="Prefix name for the output files.")
    parser.add_argument('-d', '--drop_first', default=True, metavar='',
                        help="Boolean; if True, drops first column of input file.\n\n")

    args = parser.parse_args()

    datafile = args.datafile
    out_prefix = args.out_prefix
    indexes = args.indexes
    drop_first = args.drop_first

    df = read_csv_dropcol(datafile, drop_first_col=drop_first)
        
    # default output name is the input filename
    if out_prefix == "": out_prefix = datafile[:-4]
    
    if indexes != "":
        try:
            indexes = pd.read_csv(indexes)
            idx_1, idx_2 = indexes.iloc[:,:2].values.T
        except FileNotFoundError:
            print("Taking index pair provided")
            #idx_1, idx_2 = ("23,56").split(",")
            idx_1, idx_2 = map(int, (indexes).split(",")) # as int values
        
    else: # indexes == ""
        #spike1_idx = 70 # first index = 35 seconds
        #min2_idx = find_all_bottoms_idx(df) # second index
        print("ERROR: Search for indexes not implemented;\n",
              "       provide csv file with indexes.\n")
        sys.exit()
        
    # Make lists with linear fit parameters ( a*x + b )
    slopes, y_inter = find_slope_all(df, idx_1, idx_2)    
    
    # Create csv file: 
    csvfile = create_csv_slopes(out_prefix, idx_1, idx_2, slopes, y_inter)

    title = datafile.split("/")[-1]
    fig = plotly_df_slopes(df, csvfile, title=title[:-4])

    # saves figure in html
    new_html = csvfile[:-4] + ".html"
    fig.write_html(file=new_html, auto_play=False)
    print(f"INFO {script}: New file created - '{new_html}'")
    
    sys.exit()