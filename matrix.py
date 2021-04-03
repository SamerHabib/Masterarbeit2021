def build(vehicleTrips, MatrixNorm):
    numberOfVehicles = len(vehicleTrips)
    F = []
    SCs = []
    for i in range(numberOfVehicles):
        for j in range(i + 1):
            sc = MatrixNorm[j][i]
            if sc > 0:
                fk = [vehicleTrips[i], vehicleTrips[j]]
                F.append(fk)
                SCs.append(sc)
                # fk.append(vIDS[i])
                # fk.append(vIDS[j])
    return F, SCs
    #for v in vehicleTrips:
     #   for fs in F:
      #      exists = v in fs
       #     valid = True
        #    if (not exists):
         #       for hn in fs:
          #          sc = MatrixNorm[v.index][hn.index]
           #         if not (sc > 0):
            #            valid = False
             #           break
              #  if (valid):
               #     fs2 = fs.copy()
                #    fs2.append(v)
                 #   F.append(fs2)
    #return F