import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

class pp():
    def __init__(self):
        mpl.rcParams['legend.fontsize'] = 10
        self.m =  mpl.rcParams['legend.fontsize']
        self.fig = plt.figure()
        self.ax = self.fig .gca(projection='3d')

    def plotLine(self, points):
        x = []
        y = []
        z = []
        for p in points:
            x.append(p[0])
            y.append(p[1])
            z.append(p[2])
        self.ax.plot(x, y, z)

    def Show(self):
        plt.show()
