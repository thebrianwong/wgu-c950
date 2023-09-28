from timeUtils import *


class Truck:
    def __init__(self, id, maxCapacity=16, speed=18):
        self.truckId = id
        self.driver = None
        self.maxCapacity = maxCapacity
        self.speed = speed
        self.packageLoad = []
        self.currentLocation = "4001 South 700 East"
        self.visitedLocations = ["4001 South 700 East"]
        # number of minutes at 8:00 AM
        self.currentTime = 480
        self.distance = 0

    def hasDriver(self):
        return True if self.driver is not None else False

    def addDriver(self, driver):
        self.driver = driver

    def canLoadPackage(self):
        return len(self.packageLoad) < self.maxCapacity

    def loadTruck(self, id):
        if not self.canLoadPackage():
            print(f"Truck No. {self.truckId} can't fit any more packages!!!")
            return False
        self.packageLoad.append(id)

    def getTruckTimeMins(self):
        return self.currentTime

    def getTruckTimeString(self):
        return minsToTimeString(round(self.currentTime))

    def updateTruckTime(self, addedTime):
        self.currentTime += addedTime

    def getTruckDistance(self):
        return self.distance

    def updateTruckDistance(self, addedDistance):
        self.distance += addedDistance

    def _calculateTime(self, distance):
        time = distance / self.speed * 60
        return time

    def travelToLocation(self, locationName, traveledDistance):
        travelTime = self._calculateTime(traveledDistance)
        self.updateTruckTime(travelTime)
        self.updateTruckDistance(traveledDistance)
        self.currentLocation = locationName
        self.visitedLocations.append(locationName)

    def resetVisitedLocations(self):
        self.visitedLocations = []
