#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: servindc
"""
from roifile import ImagejRoi
from shapely.geometry import Polygon

def str2polygon(filename):
    roi_path = Path(filename)
    imagej_roi = ImagejRoi.fromfile(roi_path)
    return Polygon(imagej_roi.coordinates())

################################################################################
if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser, RawTextHelpFormatter
    import textwrap
    from pathlib import Path
    #from zipfile import ZipFile
    import plotly.graph_objects as go
    import plotly.io as pio
    pio.templates.default='plotly_dark'
    
    print("")
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
    if output_dir != "":
        out_path = Path(output_dir)
        out_path = out_path.parent.joinpath(out_path.stem).with_suffix(".html")
    else:
        new_html = f"plotly_{rois_path.name}.html"
        out_path = rois_path.parent.joinpath(new_html)
    
    if rois_path.suffix == ".zip":
        print("INFO Only unzipped directories as input")
        sys.exit()
        # unzipped = rois_path.parent.joinpath(rois_path.stem)
        # if not unzipped.exists():
        #     # unzip folder
        #     with ZipFile(rois_path, 'r') as zip:
        #         zip.extractall(path=unzipped)
        #     print(f"\nINFO Creating unzipped folder: {unzipped}\n")
        # else:
        #     print(f"\nINFO Using existing folder: {unzipped}\n")
        # rois_path = unzipped

    # list of all .roi filenames - alphabetycal order
    roi_files = sorted(rois_path.glob("*.roi"))
    
    # new figure
    fig = go.Figure(layout=go.Layout(title=rois_path.name))
    for i, r in enumerate(roi_files):
        # roi object
        #imagej_roi = ImagejRoi.fromfile(r)
        # polygon object
        #pol = roi2polygon(imagej_roi)
        pol = str2polygon(r)
        X, Y = pol.exterior.xy
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
    #new_html = f"rois_plotly_{rois_path.name}.html"
    #
    #new_file = out_path.joinpath(new_html)
    fig.write_html(file=out_path, auto_play=False)
    print(f"\nINFO Created new file: {out_path}\n")
    
    sys.exit()
################################################################################