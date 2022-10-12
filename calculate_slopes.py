#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: servindc
"""

import numpy as np
import pandas as pd
import plotly.express as px
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
		print("find_bottom(): 'a' must be smaller than 'b'.")
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
			idx_dx = find_bottom_idx(x, 280, 310, dx_treshold=dx_treshold)
		except IndexError:
			print("find_all_bottoms_dx(): IndexError")
			idx_dx = 0
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
	print(f"create_csv_slopes(): Created file - '{new_name}'")
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
		z = df.iloc[:,i]
		s, m, a, b = df_slopes.iloc[i,:] # spike, min, ax+b
		line = z[int(s):int(m)]
		def f(x): return (a)*x+b
		fig.add_trace(go.Scatter(x=df.index, y=z, line=dict(color="#0069b9"), ),
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
	
	fig.update_layout(title_text="<b>"+title+"</b>", showlegend=False,
					height=350*n_rows, width=350*n_cols, # 5*n_cols, 4*n_rows
					margin=dict(l=20, r=20, t=80, b=20),
					) # yaxis_range=[y_min-100,y_max+100],
	return fig

################################################################################

if __name__ == "__main__":
	import sys
	from argparse import ArgumentParser
	#from pathlib import Path
	#from datetime import date

	print("")

	usage = (
		"%(prog)s datafile.csv [-h] [-o] [-i] "
		)

	parser = ArgumentParser(
		description="""	Calculates slope between indexes, for each column of the given datafile
						and plots it; the title graph is the input filename.
						\n\n""",
		usage=usage)
	
	parser.add_argument('datafile', type=str,
						help="Data file (csv format).")
	parser.add_argument('-o', '--out_prefix', default='', metavar='',
						help="Prefix name for the output files.")
	parser.add_argument('-i', '--indexes', type=str, default='', metavar='',
						help="Filename with the indexes of point1 & point2.")

	args = parser.parse_args()

	datafile = args.datafile
	out_prefix = args.out_prefix
	indexes = args.indexes

	df = read_csv_dropcol(datafile)

	# default output name is the input filename
	if out_prefix == "": out_prefix = datafile[:-4]
	if indexes == "":
		spike1_idx = 70 # first index = 35 seconds
		min2_idx = find_all_bottoms_idx(df) # second index

	slopes, y_inter = find_slope_all(df, spike1_idx, min2_idx)	
	csvfile = create_csv_slopes(out_prefix, spike1_idx, min2_idx, slopes, y_inter)

	title = datafile.split("/")[-1]
	fig = plotly_df_slopes(df, csvfile, title=title[:-4])

	# saves figure in html
	new_html = csvfile[:-4] + ".html"
	fig.write_html(file=new_html, auto_play=False)
	print(f"calculate_slopes.py: New file created - '{new_html}'")

	sys.exit()