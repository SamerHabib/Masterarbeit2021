from neo4j import GraphDatabase
from MercatorProjection import geodetic_to_ecef
from VehicleTrip import VehicleTrip


class Graph:

    def __init__(self):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "samer"))
        self.Points = []
        self.VehicleTrips = []

    def close(self):
        self.driver.close()

    def getVehicleSetTrips(self):
        with self.driver.session() as session:
            result = session.run("MATCH (n:VehicleSet) where ID(n) = 692 with n Limit 1 Match (n)-[r:CONSISTS_OF]->(rp:Vehicle) with rp"
                                  " MATCH (rp)-[:START_AT]->(n1:RoadPoint), (rp)-[:END_AT]->(n2:RoadPoint)"
                                  " CALL algo.shortestPath.stream(n1, n2, 'distance',{relationshipQuery:'ROAD_SEGMENT'})"
                                  " YIELD nodeId, cost"
                                  " RETURN algo.getNodeById(nodeId) as Node, ID(rp) as Id ")
            records = []
            for record in result:
                records.append(record)
            #pointsLine = []
            v = VehicleTrip()
            index = -1
            for rec in records:
                if v.id != rec[1] or rec == records[len(records) - 1]:
                    if v.id != None:
                        v.orgin = pointsLine[0]
                        v.end = pointsLine[len(pointsLine) - 1]
                        v.points = pointsLine
                        self.VehicleTrips.append(v)
                    v = VehicleTrip()
                    v.id = rec[1]
                    index = index + 1
                    v.index = index
                    pointsLine = []
                lat = rec[0].get("lat")
                lon = rec[0].get("lon")
                r = None
                x, y, z = geodetic_to_ecef(lat, lon, 0)
                z = 0
                p1 = (x, y, z)
                pointsLine.append(p1)

    def getVTripbyID(self, id):
        matches = next(x for x in self.VehicleTrips  if x.id == id)

        matches.drawLine(2)