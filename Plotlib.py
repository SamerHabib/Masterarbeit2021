import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure()
ax = fig.gca(projection='3d')

def plotLine(points):
    x = []
    y = []
    z = []
    for p in points:
        x.append(p[0])
        y.append(p[1])
        z.append(p[2])
    ax.plot(x, y, z)

def Show():
    plt.show()
