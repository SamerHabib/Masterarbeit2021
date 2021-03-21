import numpy

from Classifying import classifyTheLineSegments, computeScore
from Graph import *
from Partitioning import findoptimalpartition
from multiprocessing import Pool

if __name__ == '__main__':
    g = Graph()
    g.getVehicleSetTrips()

    v = VehicleTrip(0,0, (0,0,0), (10,10,10), )
    pool = Pool()  # Create a multiprocessing Pool
    listV = pool.map(findoptimalpartition, g.VehicleTrips)
    pool.close()

    allLineSegments = []
    for x in listV:
        allLineSegments += x.getLineSegments()

    allSet = classifyTheLineSegments(allLineSegments)

    numberOfVehicles = len(g.VehicleTrips)
    matrix = numpy.zeros(shape=(numberOfVehicles, numberOfVehicles))

    for set in allSet:
        computeScore(set, matrix)

    MatrixNorm = matrix / numpy.abs(matrix).max()

    F = []
    allV = g.VehicleTrips
    for i in range(numberOfVehicles):
        for j in range(i + 1):
            sc = MatrixNorm[j][i]
            if sc > 0:
                fk = [allV[i], allV[j]]
                F.append(fk)
                # fk.append(vIDS[i])
                # fk.append(vIDS[j])
    for v in g.VehicleTrips:
        for fs in F:
            exists = v in fs
            valid = True
            if (not exists):
                for hn in fs:
                    sc = MatrixNorm[v.index][hn.index]
                    if not (sc > 0):
                        valid = False
                        break
                if (valid):
                    fs2 = fs.copy()
                    fs2.append(v)
                    F.append(fs2)

    i = 0





