#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: servindc
"""

from roifile import ImagejRoi
from shapely.geometry import Polygon

import plotly.graph_objects as go
#from plotly.subplots import make_subplots
import plotly.io as pio
pio.renderers.default='browser'

def str2roi(filename):
    roi_path = Path(filename)
    return ImagejRoi.fromfile(roi_path)

def roi2polygon(imagej_roi):
    return Polygon(imagej_roi.coordinates())

def str2polygon(filename):
    return roi2polygon(str2roi(filename))

################################################################################
if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser, RawTextHelpFormatter
    import textwrap
    from pathlib import Path
    import numpy as np
    
    print("")
    #script = f"{__file__.split('/')[-1]}"
    script = Path(__file__).name
    
    usage = ("%(prog)s folder_with_roi_files [-h] [-o]")
    
    description = """
    Creates an interactive plot for the .roi files inside the given directory.
        """
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter,
        description=textwrap.dedent(description), usage=usage)
    
    parser.add_argument('rois_dir', type=str,
                        help="Directory with ROI files")
    parser.add_argument('-o', '--output_dir', default='', metavar='',
                        help="Output directory name for the output files.")
    args = parser.parse_args()
    
    rois_dir = args.rois_dir
    output_dir = args.output_dir
    
    # path object
    rois_path = Path(rois_dir)
    out_path = Path(output_dir)
    # list of all .roi filenames - alphabetycal order
    roi_files = sorted(rois_path.glob("*.roi"))
    
    # new figure
    fig = go.Figure(layout=go.Layout(title= rois_dir))
    for i, r in enumerate(roi_files):
        # roi object
        #imagej_roi = ImagejRoi.fromfile(r)
        # polygon object
        #pol = roi2polygon(imagej_roi)
        pol = str2polygon(r)
        X, Y = pol.exterior.xy
        print(r.name, " ", int(np.mean(Y)), int(np.mean(X)))
        
        polygon = go.Scatter(
            x=list(X),
            y=list(Y),
            name = r.name, # basename
            #showlegend=False,
            mode="lines",
            fill="toself",
            line=dict(color="cornflowerblue", width=2),
            )
        fig.add_trace(polygon)
    #fig.show()
    new_html = "rois_plotly.html"
    fig.write_html(file=out_path.joinpath(new_html), auto_play=False)
    
    sys.exit()
################################################################################



