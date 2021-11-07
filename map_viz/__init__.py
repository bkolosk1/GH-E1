import os

MODULE_ROOT = os.path.dirname(os.path.abspath(__file__)) # module root
DATA_DIR = os.path.abspath(os.path.join(MODULE_ROOT, "data"))

from map_viz.src.map import MapPlot