#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: servindc
"""
from pathlib import Path
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
    import numpy as np
    
    print("")
    #script = f"{__file__.split('/')[-1]}"
    script = Path(__file__).name
    
    usage = ("%(prog)s inner_roi outer_roi [-h] [-o]")
    
    description = """
    Checks if the first ROI it's a subset of the second ROI
        """

    parser = ArgumentParser(formatter_class=RawTextHelpFormatter,
        description=textwrap.dedent(description), usage=usage)
    
    parser.add_argument('inner_roi', type=str,
                        help="Inner ROI filename")
    parser.add_argument('outer_roi', type=str,
                        help="Outer ROI filename")
    parser.add_argument('-o', '--output_dir', default='', metavar='',
                        help="Output directory name for the output files.")
    args = parser.parse_args()
    
    inner_roi = args.inner_roi
    outer_roi = args.outer_roi
    output_dir = args.output_dir
    # path objects
    inner_path = Path(inner_roi)
    outer_path = Path(outer_roi)
    # polygon objects
    inner_pol = str2polygon(inner_path)
    outer_pol = str2polygon(outer_path)
    
    print(f"INFO inner roi - {inner_path}")
    print(f"INFO outer roi - {outer_path}")
    
    if outer_pol.contains(inner_pol):
        print("INFO The inner ROI is fully contained in the outer ROI\n")
        sys.exit()
    
    print("INFO Creating new roi for the inner file")
    # new_inner = (inner_roi) n (outer_roi)
    new_inner = inner_pol.intersection(outer_pol)

    # new ROI object
    try: x, y = new_inner.boundary.xy
    except (ValueError, NotImplementedError):
        i = np.argmax([ g.area for g in new_inner.geoms ])
        new_inner = new_inner.geoms[i]
        x, y = new_inner.boundary.xy
    new_roi = ImagejRoi.frompoints( np.array([x,y]).T )

    if output_dir == "":
        new_name = inner_path.stem + "" + inner_path.suffix
        out_path = inner_path.parent.joinpath(new_name)
    else:
        out_path = Path(output_dir)
    # save as ROI file
    new_roi.tofile(filename=out_path)
    print(f"INFO Created new file: {out_path}")
    c = round((inner_pol.area - new_inner.area)/inner_pol.area*100,2)
    print(f"INFO Area changed in {c}%\n")
    
    sys.exit()

# TESTS

inner_roi = "../data/ROIS3/monocapa/UTP/ROIs/ROI_UTP[-8]_201119_3_nucleus/n10_0001-0156-0272.roi"
outer_roi = "../data/ROIS3/monocapa/UTP/ROIs/ROI_UTP[-8]_201119_3_wholecell/c10_0001-0156-0273.roi"

inner_path = Path(inner_roi)
outer_path = Path(outer_roi)

#---

outer_pol = outer_pol.buffer(0)

x, y = outer_pol.boundary.xy
new_out = ImagejRoi.frompoints( np.array([x,y]).T )
new_out.tofile(filename=outer_roi)



inner_pol = inner_pol.buffer(0)




i = np.argmax([ g.area for g in outer_pol.geoms ])
outer_pol = outer_pol.geoms[i]




x,y = new_inner.boundary[0].xy


