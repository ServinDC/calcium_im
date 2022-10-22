#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: servindc
"""
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

def plotly_df(df, title=""):
    "Plots a dataframe with the slopes calculated, multiple subplots"
    n = len(df.columns)
    n_cols = 4
    n_rows = n//n_cols + bool(n%n_cols) # +1 row if n%cols not zero

    fig = make_subplots(rows=n_rows, cols=n_cols,
                        subplot_titles=[name for name in df.columns],
                        shared_yaxes=True,# rows x cols size necessary to use h_spacing
                        specs = [[{} for i in range(n_cols)] for j in range(n_rows)],
                        horizontal_spacing = 0.02, vertical_spacing = 0.03)
    for i in range(n): # plot dataframe columns
        try:
            z = df.iloc[:,i]
            fig.add_trace(go.Scatter(x=df.index, y=z,
                                     line=dict(color="#0069b9"), ),
                          row=i//n_cols+1, col=i%n_cols+1 )
        except:
            print(f"ERROR plotly_df_slopes(): while adding trace number {i}")
    fig.update_layout(title_text="<b>"+title+"</b>", showlegend=False,
                    height=350*n_rows, width=350*n_cols, # 5*n_cols, 4*n_rows
                    margin=dict(l=20, r=20, t=80, b=20),
                    )
    return fig

################################################################################

if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser, RawTextHelpFormatter
    import textwrap
    from pathlib import Path
    
    print("")
    #script = f"{__file__.split('/')[-1]}"
    script = Path(__file__).name
    
    usage = ("%(prog)s datafile.csv [-h] [-o] [-d]")
    
    description = """
    Creates a plot for each column of the given datafile, using plotly;
    the title graph is the input filename. New file created:
        "*.html" - file with interactive plots.
        """

    parser = ArgumentParser(formatter_class=RawTextHelpFormatter,
        description=textwrap.dedent(description), usage=usage)
    
    parser.add_argument('datafile', type=str,
                        help="Data file (csv format).")
    parser.add_argument('-o', '--out_prefix', default='', metavar='',
                        help="Prefix name for the output files.")
    parser.add_argument('-d', '--drop_first', default=True, metavar='',
                        help="Boolean; if True, drops first column of input file.\n\n")
    args = parser.parse_args()

    datafile = args.datafile
    out_prefix = args.out_prefix
    drop_first = args.drop_first
    
    df = read_csv_dropcol(datafile, drop_first_col=drop_first)
    filepath = Path(datafile)
        
    # default output name is the input filename
    if out_prefix == "": out_prefix = datafile[:-4]

    fig = plotly_df(df, title=filepath.stem) # filename without extentsion

    # saves figure in html
    new_html = out_prefix + ".html"
    fig.write_html(file=new_html, auto_play=False)
    print(f"INFO {script}: New file created - '{new_html}'")
    
    sys.exit()