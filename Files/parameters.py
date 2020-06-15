import time # We want to know how long the program runs
import datetime
import math

"""
import matplotlib.pyplot as plt # Visualise data #keep as comment for now

## build a QApplication before building other widgets
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
import sys
"""

"""
/!\ before installing anithing be sure you have pip, write:
$ python -m pip install -U pip

In order to install matplotlib write the following command lines (fist installs pip, second installs matplotlib):
$ python -m pip install -U matplotlib

In order to install pyqtgraph, write (stable version for windows):
$ pip install pyqtgraph==0.11.0rc0
But pyqtgraph requires PyQt5, write:
$ pip install PyQt5
In order to plot 3D points you will need PyOpenGL, write:
$ pip install PyOpenGL
"""

# Constants
XS = 9238.847; YS = 3476.316; ZS = 1387.083 #S9 total station position in meters
V0 = 19.8120 #gon
COEFF_J = 278.77885605
COEFF_N = 80.65533842
PI = math.pi

#list
param = [None] * 32 #There are max 32 elements on one row

#list of 2D lists [Name, Value]. Use the FindValueByName(name, list) to find the value linked to the name or change it with ChangeValueByName(name, n, l)
prismParam = [["number", None], ["prisme", None],
["GPSwk", None], ["DOWk", None], ["SOWk", None], ["SatNumber", None],
["Pos", None], ["DI", None], ["SigDist", None], ["hpDI", None],
["Alpha", None], ["SigAH", None], ["Beta", None],
["SigAV", None], ["hpAV", None], ["CstPrisme", None],
["IndicRef", None], ["Meteoppm", None], ["Extra", None],
["x", None], ["y", None], ["z", None],
["dx", None], ["dy", None], ["dz", None],
["Pression", None], ["Temp", None],
["coeff3", None], ["coeff4", None], ["coeff5", None], ["coeff6", None], ["coeff7", None],["coeff8", None]]
#x:East, y:North, z:Elevation