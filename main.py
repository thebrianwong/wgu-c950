# C950, Brian Wong, 011147336
from package_importer import import_package
from distance_import import import_distance
from truck import Truck
from driver import Driver

package_hash_table, special_notes_array, early_delivery_array = import_package("package.csv")
distance_map = import_distance("distance.csv")


# print(special_notes_array)
# print(early_delivery_array)
def load_truck_at_hub(truck):
    # format truck time as "XX:XX XM" to update package's load times as time strings
    truck_time_mins = truck.get_truck_time_mins()
    truck_time_string = truck.get_truck_time_string()
    special_ids_to_remove = []
    for package_id in special_notes_array:
        package = package_hash_table.lookup_package(package_id)

        # add some logic to handle package id 9
        # use utils to determine if truck's current time is after 10:20AM (when address gets fixed)
        # if so, load the package (probably doesn't matter which truck)
        if package_id == 9:
            # 10:20 AM in number of minutes
            time_when_address_fixed = 620
            if truck_time_mins >= time_when_address_fixed:
                truck.load_truck(package_id)
                package.update_loading_time(truck_time_string)
                package.update_status("En Route")
                package.update_delivered_by(truck.truckId)

                special_ids_to_remove.append(package_id)

        # only load delayed packages to Truck 1 as Truck 1 will intentionally depart later than Truck 2
        if truck.truckId == 1 and "Delayed on flight" in package.lookup_notes():
            truck.load_truck(package_id)
            package.update_loading_time(truck_time_string)
            package.update_status("En Route")
            package.update_delivered_by(truck.truckId)

            # remove from array to prevent duplicates since the package has been loaded
            special_ids_to_remove.append(package_id)
            if package_id in early_delivery_array:
                early_delivery_array.remove(package_id)

        elif truck.truckId == 2:
            # skip 3 on initial load since it has EOD delivery and
            # room needs to be made for 40
            if truck_time_string == "8:00 AM" and package_id == 3:
                continue
            if "Can only be on truck 2" in package.lookup_notes():
                truck.load_truck(package_id)
                package.update_loading_time(truck_time_string)
                package.update_status("En Route")
                package.update_delivered_by(truck.truckId)

                special_ids_to_remove.append(package_id)
                if package_id in early_delivery_array:
                    early_delivery_array.remove(package_id)

            elif "Must be delivered with" in package.lookup_notes():
                # parse special notes for packages that have to be delivered together
                split_string = package.lookup_notes().split(" ")
                first_package_id = int(split_string[4].replace(",", ""))
                first_package = package_hash_table.lookup_package(first_package_id)
                second_package_id = int(split_string[5])
                second_package = package_hash_table.lookup_package(second_package_id)

                special_ids_to_remove.append(package_id)
                if package_id in early_delivery_array:
                    early_delivery_array.remove(package_id)

                truck.load_truck(package_id)
                package.update_loading_time(truck_time_string)
                package.update_status("En Route")
                package.update_delivered_by(truck.truckId)
                if package_id in early_delivery_array:
                    early_delivery_array.remove(package_id)

                if first_package_id not in truck.package_load:
                    truck.load_truck(first_package_id)
                    first_package.update_loading_time(truck_time_string)
                    first_package.update_status("En Route")
                    first_package.update_delivered_by(truck.truckId)
                    if first_package_id in early_delivery_array:
                        early_delivery_array.remove(first_package_id)

                if second_package_id not in truck.package_load:
                    truck.load_truck(second_package_id)
                    second_package.update_loading_time(truck_time_string)
                    second_package.update_status("En Route")
                    second_package.update_delivered_by(truck.truckId)
                    if second_package_id in early_delivery_array:
                        early_delivery_array.remove(second_package_id)

    # now that the iteration of the special notes array is done
    # remove all the package ids that were loaded
    for id in special_ids_to_remove:
        special_notes_array.remove(id)

    # load early delivery packages to Truck 2 since it will leave at 8:00 AM
    if truck.truckId == 2:
        early_ids_to_remove = []
        for package_id in early_delivery_array:
            if truck.can_load_package():
                package = package_hash_table.lookup_package(package_id)
                truck.load_truck(package_id)
                package.update_loading_time(truck_time_string)
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

    for raw_package in reversed(package_hash_table):
        package_id = raw_package[0].id
        package = package_hash_table.lookup_package(package_id)
        if (package.lookup_loading_time() == "Not Loaded Yet" and package_id not in special_notes_array
                and package_id not in early_delivery_array):
            if truck.can_load_package():
                truck.load_truck(package_id)
                package.update_loading_time(truck_time_string)
                package.update_status("En Route")
                package.update_delivered_by(truck.truckId)

                if package_id in special_notes_array:
                    special_notes_array.remove(package_id)
                if package_id in early_delivery_array:
                    early_delivery_array.remove(package_id)
            else:
                break


def find_next_location_and_distance(truck):
    closest_new_location = ""
    closest_distance = 100

    truck_current_location = truck.current_location
    truck_visited_locations = truck.visited_locations
    list_of_distances = distance_map[truck_current_location]
    for location, distance in list_of_distances.items():
        if location not in truck_visited_locations and distance < closest_distance:
            closest_new_location = location
            closest_distance = distance
    return closest_new_location, closest_distance


def deliver_truck_packages(truck):
    while len(truck.package_load) > 0:
        hub_has_more_packages = False
        next_location, distance = find_next_location_and_distance(truck)
        truck.travel_to_location(next_location, distance)

        # deliver any packages addressed to the new location
        packages_delivered = []
        for package_id in truck.package_load:
            package = package_hash_table.lookup_package(package_id)
            package_address = package.lookup_address()
            if package_address == truck.current_location:
                truck_time_string = truck.get_truck_time_string()
                package.update_status("Delivered")
                package.update_delivery_time(truck_time_string)
                packages_delivered.append(package_id)
        for package_id in packages_delivered:
            truck.package_load.remove(package_id)

        # Package 9's address gets corrected at 10:20 AM
        # 10:20 AM in minutes is 620
        address_correction_time = 620
        if truck.get_truck_time_mins() >= address_correction_time:
            package9 = package_hash_table.lookup_package(9)
            package9.update_address("410 S State St")

        # backtrack to hub as appropriate to reload packages
        # don't backtrack after delivering the initial load
        # as doing so will require the truck to traverse the
        # same locations again before driving to new locations

        # truck 1 doesn't have as big of a burden as truck 2
        # in regard to delivering packages with deadline at or
        # before 10:30 AM, so truck 1 will deliver the 8 packages
        # that were not a part of the trucks' initial loads
        if len(truck.package_load) == 7 and truck.truckId == 1:
            for raw_package in package_hash_table:
                package_id = raw_package[0].id
                package = package_hash_table.lookup_package(package_id)
                if package.lookup_loading_time() == "Not Loaded Yet":
                    hub_has_more_packages = True
                    break

        # truck 2 has to go back and load the previously skipped package 3
        if len(truck.package_load) == 15 and truck.truckId == 2:
            for raw_package in package_hash_table:
                package_id = raw_package[0].id
                package = package_hash_table.lookup_package(package_id)
                if package.lookup_loading_time() == "Not Loaded Yet":
                    hub_has_more_packages = True
                    break

        if hub_has_more_packages:
            hub_address = "4001 South 700 East"
            truck_current_location = truck.current_location
            distance_to_hub = distance_map[truck_current_location][hub_address]
            print(distance_to_hub)

            truck.reset_visited_locations()
            truck.travel_to_location(hub_address, distance_to_hub)
            load_truck_at_hub(truck)


truck1 = Truck(1)
truck2 = Truck(2)
truck3 = Truck(3)

driver1 = Driver("Bimmy")
driver2 = Driver("Jimmy")

truck1.add_driver(driver1)
truck2.add_driver(driver2)

# Truck 1 will wait for the delayed packages and depart at 9:05 AM
# waiting from 8:00 AM to 9:05 AM takes 65 minutes
truck1.update_truck_time(65)

load_truck_at_hub(truck2)
load_truck_at_hub(truck1)

print(truck1.package_load, "truck 1", len(truck1.package_load))
print(truck2.package_load, "truck 2", len(truck2.package_load))

deliver_truck_packages(truck2)
print(truck2.get_truck_distance(), truck2.get_truck_time_string())

deliver_truck_packages(truck1)
print(truck1.get_truck_distance(), truck1.get_truck_time_string())

notLoaded = 0
for raw_package in package_hash_table:
    package_id = raw_package[0].id
    package = package_hash_table.lookup_package(package_id)
    if package.lookup_loading_time() == "Not Loaded Yet":
        notLoaded += 1
    print(
        f"Package ID: {package_id} | {package.lookup_address()} | Loading Time: {package.lookup_loading_time()} | "
        f"Delivery Time: {package.lookup_delivery_time()} | Deadline: {package.lookup_deadline()} | "
        f"Status: {package.lookup_delivery_status()} | {package.lookup_delivered_by()}")
print(notLoaded)
print(special_notes_array)
