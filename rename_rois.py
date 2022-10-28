#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: servindc
"""
from pathlib import Path
from roifile import ImagejRoi
from shapely.geometry import Polygon, Point
import shutil

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
    
    print("")
    #script = f"{__file__.split('/')[-1]}"
    script = Path(__file__).name
    
    usage = ("%(prog)s folder_with_roi_files [-h] [-o]")
    
    description = """
    For the .roi files inside the given directory, finds which ones are cell or
    nucleus ROIs, and renames them accordingly:
        cells:      nucleus:
        c01_*.roi   n01_*.roi
        c02_*.roi   n01_*.roi
        c03_*.roi   n01_*.roi
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
    print(f"INFO Founded {len(roi_files)} roi files in the given directory.\n")
    # Create dictionaries
    roi_areas = {}              # {fname: roi_area}
    roi_centroid = {}           # {fname: centroid}
    roi_poly = {}               # {fname: polyygon}
    for fname in roi_files:
        p = str2polygon(fname)
        roi_poly[fname.name] = p
        roi_areas[fname.name] = p.area  # tmp list
        roi_centroid[fname.name] = [x[0] for x in p.centroid.xy]
    # Finds pair correspondence
    roi_pairs = {}
    while len(roi_areas) != 0:
        # get key with max value, which must be a cell roi
        max_value_key = max(roi_areas, key=roi_areas.get)
        roi_areas.pop(max_value_key)    # deletes current pair with max_value_key
        p = roi_poly[max_value_key]
        for key in roi_areas:
            c = Point(roi_centroid[key])
            # if the roi centroid is contained in the cell roi
            if p.contains(c):
                roi_pairs[max_value_key] = key
                roi_areas.pop(key)
                break
    # Creates output directory
    try: out_path.mkdir()
    except FileExistsError:
        print(f"INFO Output directory already exists: '{out_path}'\n")
    # Do the re-naming
    for i, key in enumerate(roi_pairs):
        # create new filenames (basename only)
        new_roi_cell = f"c{i+1:02}_" + key
        new_roi_nucl = f"n{i+1:02}_" + roi_pairs[key]
        # new full paths
        new_cell = out_path.joinpath(new_roi_cell)
        new_nucl = out_path.joinpath(new_roi_nucl)
        # old full paths
        old_cell = rois_path.joinpath(key)             # cell
        old_nucl = rois_path.joinpath(roi_pairs[key])  # nucleus
        # copy file contents
        s = shutil.copy(old_cell, new_cell)
        print(f"INFO Created new file: {s}")
        s = shutil.copy(old_nucl, new_nucl)
        print(f"INFO Created new file: {s}\n")

    sys.exit()
