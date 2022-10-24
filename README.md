# calcium_im
Python scripts to analyze the response signals of calcium imaging data.

Libraries needed: `numpy`, `pandas`, `plotly`, `scipy`.

script|description| raw file link
-----:|:----------|:------------:
`calculate_slopes.py`| Calculates the slope of the linear fit between the provided indexes.| [**link**](https://raw.githubusercontent.com/ServinDC/calcium_im/main/calculate_slopes.py)
`plotly_df.py`| Creates interactive plots of a csv dataframe. | [**link**](https://raw.githubusercontent.com/ServinDC/calcium_im/main/plotly_df.py)
`unbleaching.py`| Decreases the magnitude of the photobleaching effect. | [**link**](https://raw.githubusercontent.com/ServinDC/calcium_im/main/unbleaching.py)

To download a script, click the _raw file link_ and save it with **`ctrl`** + **`S`**.

## Scripts

### `calculate_slopes.py`

<details>
<summary><b>More info</b></summary>

Calculates slope between indexes, for each column of the given datafile and plots it; the title graph is the input filename.
New files created:

"`*_slopes.html`" - file with interactive plots.
"`*_slopes.csv`" - file with slope & y-intercept values.

**Example use:**

Printing the script help:
```bash
python ./calculate_slopes.py -h
```
Using a file with a index pair for each datafile column:
```bash
python ./calculate_slopes.py datafile.csv -i datafile_idx.csv
```
Using the same index pair for each column:
```bash
python ./calculate_slopes.py datafile.csv -i "8,15"
```
<details>
<summary><b>Example files</b></summary>

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
</details>
</details>

---

### `plotly_df.py`

<details>
<summary><b>More info</b></summary>

Printing the script help:
```bash
python ./plotly_df.py -h
```
</details>

---

### `unbleaching.py`

<details>
<summary><b>More info</b></summary>

Printing the script help:
```bash
python ./unbleaching.py -h
```
</details>