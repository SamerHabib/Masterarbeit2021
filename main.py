import copy

import numpy

from Classifying import *
from Graph import *
from Optimization import *
from Partitioning import findoptimalpartition
from LinearRegression import *
from multiprocessing import Pool
import time
import matplotlib.pyplot as plt

from Plotlib import *
from matrix import build

if __name__ == '__main__':
    start_time = time.time()
    print("---Start %s seconds ---" % (time.time() - start_time))
    g = Graph()
    g.getVehicleSetTrips()
    vehicleTrips = g.VehicleTrips
    v = copy.deepcopy(vehicleTrips[6])
    v.index = 0
    v.id = 0
    v1 = copy.deepcopy(vehicleTrips[7])
    v1.index = 1

    vehicleTrips = [v,v1]


    pp = pp()
    pp.plotLine(vehicleTrips[0].points)
    pp.plotLine(vehicleTrips[1].points)
    pp.Show()

    print("---intial  %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    pool = Pool()  # Create a multiprocessing Pool
    listV = pool.map(findoptimalpartition, vehicleTrips)
    pool.close()

    allLineSegments = []
    for x in listV:
        x.calcDistance()
        allLineSegments += x.getLineSegments()
        #x.drLines()
        #x.parLines()
    print("---Partition %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    numberOfVehicles = len(vehicleTrips)
    allSet, matrixper = classifyTheLineSegments(allLineSegments, numberOfVehicles)
    print("---Classify %s seconds ---" % (time.time() - start_time))
    start_time = time.time()

    matrixprozent = numpy.zeros(shape=(numberOfVehicles, numberOfVehicles))
    matrix = numpy.zeros(shape=(numberOfVehicles, numberOfVehicles))

    for set in allSet:
        #p =pp()
        #for l in set:
         #   p.plotLine([l.startpoint, l.endpoint])
        #p.Show()
        computeScore2(set, matrix, matrixprozent)

    matrix1 = matrix * 0.1


    matrixd = matrix1  #numpy.subtract(matrix1, matrixper)
    matrixd1 = matrixd.clip(min=0)
    matrixpfff= numpy.zeros(shape=(numberOfVehicles, numberOfVehicles))
    for i in range(numberOfVehicles):
        for j in range(i + 1):
            sc = matrixd1[j][i]
            if sc > 0:
                sss = (listV[i].distance + listV[j].distance) /2
                matrixpfff[j][i] = matrixd1[j][i] / sss
                matrixpfff[i][j] = matrixd1[i][j] / sss

    #MatrixNorm = matrixd1 / numpy.abs(matrixd1).max()


    #where_are_NaNs = numpy.isnan(matrixd)
    #matrixd[where_are_NaNs] = 0

    #MatrixNorm = matrix / numpy.abs(matrix).max()
    #MatrixNorm1 = matrixper / numpy.abs(matrixper).max()

    Groups = []
    scs = []
    Groups, scs = build(vehicleTrips, matrixpfff)
    print("---Groups %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    # use "definitions()" to create own network
    # road network import
    road_network, saving_factor, every_value = definitions()
    #vvv = VehicleTrip()
    #vvv.id = 700
    #vvv.orginId = vehicleTrips[1].orginId
    #vvv.endId = vehicleTrips[1].endId
    #fk = [vehicleTrips[8], vehicleTrips[6]]
    # use Neo4jConnection to use a neo4j database
    road_network, group, vehicle_locations = g.get_data()

    #print("------------------------------------------------------------------------------")
    #model, x, y = optimization_model(road_network, fk, 0.1)
    #print("----------------------------------------------------")
    #model1, x1, y1 = optimization_model(road_network, fk, 0)
    #output_text(road_network, fk, model, x, y, every_value)
    xx = []
    xx += scs
    yy = []
    # run the model and return variables and model
    matrixResult = numpy.zeros(shape=(numberOfVehicles, numberOfVehicles))
    for g in Groups:
        print("------------------------------------------------------------------------------")
        model, x, y = optimization_model(road_network, g, saving_factor)
        objSave = model.ObjBound
        print("----------------------------------------------------")
        model1, x1, y1 = optimization_model(road_network, g, 0)
        objs = model1.ObjBound
        yx = (objs - objSave)/(objs/2)
        matrixResult[g[0].index][g[1].index] += yx
        yy.append(yx)
        # generate output
        #output_text(road_network, g, model, x, y, every_value)
    plotLinearReg(xx, yy)
    #toWrite = np.column_stack((xx, yy))
    #np.savetxt('vs3255.txt', toWrite)
    print("---Opt %s seconds ---" % (time.time() - start_time))
    i = 0





