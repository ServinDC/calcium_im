#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: servindc
"""
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import linregress

def read_csv_dropcol(filename, drop_first_col=True):
    "Reads a csv file droping its first column"
    if drop_first_col==True:
        # sets first named column as the index column (drops first idx column)
        df = pd.read_csv(filename, index_col=0)
        # resets the index to begin with zero
        df.reset_index(drop=True, inplace=True)
        return df
    return pd.read_csv(filename)

def exp_func(x, a, b, c):
  #if -value > np.log(np.finfo(type(value)).max)
  return np.exp(-b * x + a) + c

def photobleach_fit(y_sample, model='exp', maxfev=2000):
  x = np.arange(0, len(y_sample))
  if model=='linear':
    m, b, r, p, std_err = linregress(x, y_sample)
    y_fit = (m*x + b)
    args = [m, b]
  elif model=='exp':  # why: y/min(y) ?
    p_opt, p_cov = curve_fit(exp_func, x, y_sample, maxfev=maxfev)
    y_fit = exp_func(x, *p_opt)
    m = -p_opt[0]*p_opt[1]  # y = a*e^{-b}), dy = -a*b
    args = p_opt
  return y_fit, args

def extrapolate(x, args, model='linear'):
    if model=='linear':
        m, b = args
        return m*x + b
    if model=='exp':
        return exp_func(x, *args)

################################################################################

if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser, RawTextHelpFormatter
    import textwrap
    from pathlib import Path
    
    print("")
    #script = f"{__file__.split('/')[-1]}"
    script = Path(__file__).name

    usage = ("%(prog)s datafile.csv [-h] [-o] [-d] [-i]")
    description = """Minimizes the bleaching effect by adding the extrapolated
    linear fitting of the initial segment of each column data.
    """
    
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter,
        description=textwrap.dedent(description), usage=usage)
    
    parser.add_argument('datafile', type=str,
                        help="Data file (csv format).")
    parser.add_argument('-o', '--out_prefix', default='', metavar='',
                        help="Prefix name for the output files.")
    parser.add_argument('-d', '--drop_first', default=True, metavar='',
                        help="If 'True', drops first column of input csv.\n\n")
    parser.add_argument('-i', '--indexes', type=str, default='', metavar='',
                        help="Start & end indexes for the curve fitting, and\
                            ending index for the extrapolation. \
                            Default values: '0,60,412'.")

    args = parser.parse_args()

    datafile = args.datafile
    out_prefix = args.out_prefix
    drop_first = args.drop_first
    indexes = args.indexes
    model = 'linear'
    
    # default output name is the input filename
    if out_prefix == "": out_prefix = datafile[:-4]
    if indexes == "":                                  # Default indexes values
        fit_idx1, fit_idx2 = 0, 60
        last_idx = 412              # index where there is no bleaching anymore
    else: # read as int values
        fit_idx1, fit_idx2, last_idx = map(int, (indexes).split(","))
       
    df = read_csv_dropcol(datafile, drop_first_col=drop_first)
    # create new array
    X = np.empty(shape=df.values.shape, dtype=np.float64)

    for i in range(len(df.columns)):
        y = df.iloc[:,i]
        y_sample = y[fit_idx1:fit_idx2+1]
        # estimate fitting curve parameters
        y_fit, args = photobleach_fit(y_sample, model=model, maxfev=2000)
        # extrapolate curve
        y_fit2 = extrapolate(x=range(len(y)), args=args, model=model)
        y_fit2[last_idx:] = y[0]
        # fill array
        X[:, i] = y + (y[0] - y_fit2)

    # create new dataframe
    df_new = pd.DataFrame(data=X, columns=df.columns).round(3)
    # save as csv file
    new_fname = out_prefix + "_ub.csv"
    df_new.to_csv(new_fname, index=False)
    print(f'\nINFO {script} Saved file: ' + new_fname + '\n')

    sys.exit()