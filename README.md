# calcium_im
Python scripts to analyze calcium imaging data.

Libraries needed:
`numpy`,
`pandas`,
`plotly`.

## Scripts

#### `calculate_slopes.py`

Calculates slope between indexes, for each column of the given datafile and plots it; the title graph is the input filename.
Creates two new files:
"*_slopes.html" - file with interactive plots.
"*_slopes.csv" - file with slope & y-intercept values.

**Example use:**

Printing the script help:
```
python ./calculate_slopes.py -h
```
Using a file with a index pair for each datafile column:
```
python ./calculate_slopes.py datafile.csv -i datafile_idx.csv
```
Using the same index pair for each column:
```
python ./calculate_slopes.py datafile.csv -i "8,15"
```

Example file `datafile.csv` with 3 columns:
```
,cell1,cell2,cell3
1,126.316,145.066,138.661
2,126.101,143.839,139.16
3,126.012,141.971,138.882
4,126.026,141.889,138.86
5,125.856,140.537,139.011
```

Example file `datafile_idx.csv` (one row per each datafile column):
```
idx1,idx2
70,307
72,300
71,305
```

---

#### `find_indexes.py`

Printing the script help:
```
python ./find_indexes.py -h
```