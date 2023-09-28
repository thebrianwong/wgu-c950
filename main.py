from package_importer import importPackage
from distance_import import importDistance
from truck import Truck
from driver import Driver

package_hash_table, special_notes_array, early_delivery_array = importPackage("package.csv")
distance_map = importDistance("distance.csv")


# print(special_notes_array)
# print(early_delivery_array)
def loadTruckAtHub(truck):
    # format truck time as "XX:XX XM" to update package's load times as time strings
    truckTimeMins = truck.getTruckTimeMins()
    truckTimeString = truck.getTruckTimeString()
    special_ids_to_remove = []
    for package_id in special_notes_array:
        package = package_hash_table.lookup_package(package_id)

        # add some logic to handle package id 9
        # use utils to determine if truck's current time is after 10:20AM (when address gets fixed)
        # if so, load the package (probably doesn't matter which truck)
        if package_id == 9:
            # 10:20 AM in number of minutes
            timeWhenAddressFixed = 620
            if truckTimeMins >= timeWhenAddressFixed:
                truck.loadTruck(package_id)
                package.update_loading_time(truckTimeString)
                package.update_status("En Route")
                package.update_delivered_by(truck.truckId)

                special_ids_to_remove.append(package_id)

        # only load delayed packages to Truck 1 as Truck 1 will intentionally depart later than Truck 2
        if truck.truckId == 1 and "Delayed on flight" in package.lookup_notes():
            truck.loadTruck(package_id)
            package.update_loading_time(truckTimeString)
            package.update_status("En Route")
            package.update_delivered_by(truck.truckId)

            # remove from array to prevent duplicates since the package has been loaded
            special_ids_to_remove.append(package_id)
            if package_id in early_delivery_array:
                early_delivery_array.remove(package_id)

        elif truck.truckId == 2:
            # skip 3 on initial load since it has EOD delivery and
            # room needs to be made for 40
            if truckTimeString == "8:00 AM" and package_id == 3:
                continue
            if "Can only be on truck 2" in package.lookup_notes():
                truck.loadTruck(package_id)
                package.update_loading_time(truckTimeString)
                package.update_status("En Route")
                package.update_delivered_by(truck.truckId)

                special_ids_to_remove.append(package_id)
                if package_id in early_delivery_array:
                    early_delivery_array.remove(package_id)

            elif "Must be delivered with" in package.lookup_notes():
                # parse special notes for packages that have to be delivered together
                splitString = package.lookup_notes().split(" ")
                firstPackageId = int(splitString[4].replace(",", ""))
                firstPackage = package_hash_table.lookup_package(firstPackageId)
                secondPackageId = int(splitString[5])
                secondPackage = package_hash_table.lookup_package(secondPackageId)

                special_ids_to_remove.append(package_id)
                if package_id in early_delivery_array:
                    early_delivery_array.remove(package_id)

                truck.loadTruck(package_id)
                package.update_loading_time(truckTimeString)
                package.update_status("En Route")
                package.update_delivered_by(truck.truckId)
                if package_id in early_delivery_array:
                    early_delivery_array.remove(package_id)

                if firstPackageId not in truck.packageLoad:
                    truck.loadTruck(firstPackageId)
                    firstPackage.update_loading_time(truckTimeString)
                    firstPackage.update_status("En Route")
                    firstPackage.update_delivered_by(truck.truckId)
                    if firstPackageId in early_delivery_array:
                        early_delivery_array.remove(firstPackageId)

                if secondPackageId not in truck.packageLoad:
                    truck.loadTruck(secondPackageId)
                    secondPackage.update_loading_time(truckTimeString)
                    secondPackage.update_status("En Route")
                    secondPackage.update_delivered_by(truck.truckId)
                    if secondPackageId in early_delivery_array:
                        early_delivery_array.remove(secondPackageId)

    # now that the iteration of the special notes array is done
    # remove all the package ids that were loaded
    for id in special_ids_to_remove:
        special_notes_array.remove(id)

    # load early delivery packages to Truck 2 since it will leave at 8:00 AM
    if truck.truckId == 2:
        early_ids_to_remove = []
        for package_id in early_delivery_array:
            if truck.canLoadPackage():
                package = package_hash_table.lookup_package(package_id)
                truck.loadTruck(package_id)
                package.update_loading_time(truckTimeString)
                package.update_status("En Route")
                package.update_delivered_by(truck.truckId)
                early_ids_to_remove.append(package_id)
            else:
                print(f"Cant load package {package_id}", truck.truckId)
                break

        # now that the iteration of the early delivery array is done
        # remove all the package ids that were loaded
        for id in early_ids_to_remove:
            early_delivery_array.remove(id)

    for rawPackage in reversed(package_hash_table):
        package_id = rawPackage[0].id
        package = package_hash_table.lookup_package(package_id)
        if (package.lookup_loading_time() == "Not Loaded Yet" and package_id not in special_notes_array
                and package_id not in early_delivery_array):
            if truck.canLoadPackage():
                truck.loadTruck(package_id)
                package.update_loading_time(truckTimeString)
                package.update_status("En Route")
                package.update_delivered_by(truck.truckId)

                if package_id in special_notes_array:
                    special_notes_array.remove(package_id)
                if package_id in early_delivery_array:
                    early_delivery_array.remove(package_id)
            else:
                break


def findNextLocationAndDistance(truck):
    closestNewLocation = ""
    closestDistance = 100

    truckCurrentLocation = truck.currentLocation
    truckVisitedLocations = truck.visitedLocations
    listOfDistances = distance_map[truckCurrentLocation]
    for location, distance in listOfDistances.items():
        if location not in truckVisitedLocations and distance < closestDistance:
            closestNewLocation = location
            closestDistance = distance
    return closestNewLocation, closestDistance


def deliverTruckPackages(truck):
    while len(truck.packageLoad) > 0:
        hubHasMorePackages = False
        nextLocation, distance = findNextLocationAndDistance(truck)
        truck.travelToLocation(nextLocation, distance)

        # deliver any packages addressed to the new location
        packagesDelivered = []
        for package_id in truck.packageLoad:
            package = package_hash_table.lookup_package(package_id)
            packageAddress = package.lookup_address()
            if packageAddress == truck.currentLocation:
                truckTimeString = truck.getTruckTimeString()
                package.update_status("Delivered")
                package.update_delivery_time(truckTimeString)
                packagesDelivered.append(package_id)
        for package_id in packagesDelivered:
            truck.packageLoad.remove(package_id)

        # Package 9's address gets corrected at 10:20 AM
        # 10:20 AM in minutes is 620
        addressCorrectionTime = 620
        if truck.getTruckTimeMins() >= addressCorrectionTime:
            package9 = package_hash_table.lookup_package(9)
            package9.update_address("410 S State St")

        # check if there are still packages at the hub
        # when the truck has delivered its initial load
        # if so, go back to the hub and reload
        # '''
        # 3 or 15 works for whatever reason, 15 is better at lil under 100
        # mb the likelihood that the closest location has a package is higher
        # when you are starting from the hub
        # upon further inspection, it seems like 3 and 15 dont delivery all packages for some reason

        # actually 2, 10 if truck 2 then truck 1
        # both have issues with not meeting some deadlines

        # if truck 1 delivers extra and length 7, then maybe, need to deliver package #3
        if len(truck.packageLoad) == 7 and truck.truckId == 1:
            for rawPackage in package_hash_table:
                package_id = rawPackage[0].id
                package = package_hash_table.lookup_package(package_id)
                if package.lookup_loading_time() == "Not Loaded Yet":
                    hubHasMorePackages = True
                    break

        if len(truck.packageLoad) == 15 and truck.truckId == 2:
            for rawPackage in package_hash_table:
                package_id = rawPackage[0].id
                package = package_hash_table.lookup_package(package_id)
                if package.lookup_loading_time() == "Not Loaded Yet":
                    hubHasMorePackages = True
                    break

        if hubHasMorePackages:
            hubAddress = "4001 South 700 East"
            truckCurrentLocation = truck.currentLocation
            distanceToHub = distance_map[truckCurrentLocation][hubAddress]
            print(distanceToHub)

            truck.resetVisitedLocations()
            truck.travelToLocation(hubAddress, distanceToHub)
            loadTruckAtHub(truck)


truck1 = Truck(1)
truck2 = Truck(2)
truck3 = Truck(3)

driver1 = Driver("Bimmy")
driver2 = Driver("Jimmy")

truck1.addDriver(driver1)
truck2.addDriver(driver2)

# Truck 1 will wait for the delayed packages and depart at 9:05 AM
# waiting from 8:00 AM to 9:05 AM takes 65 minutes
truck1.updateTruckTime(65)

loadTruckAtHub(truck2)
loadTruckAtHub(truck1)

print(truck1.packageLoad, "truck 1", len(truck1.packageLoad))
print(truck2.packageLoad, "truck 2", len(truck2.packageLoad))

deliverTruckPackages(truck2)
print(truck2.getTruckDistance(), truck2.getTruckTimeString())

deliverTruckPackages(truck1)
print(truck1.getTruckDistance(), truck1.getTruckTimeString())

notLoaded = 0
for rawPackage in package_hash_table:
    package_id = rawPackage[0].id
    package = package_hash_table.lookup_package(package_id)
    if package.lookup_loading_time() == "Not Loaded Yet":
        notLoaded += 1
    print(
        f"Package ID: {package_id} | {package.lookup_address()} | Loading Time: {package.lookup_loading_time()} | "
        f"Delivery Time: {package.lookup_delivery_time()} | Deadline: {package.lookup_deadline()} | "
        f"Status: {package.lookup_delivery_status()} | {package.lookup_delivered_by()}")
print(notLoaded)
print(special_notes_array)
