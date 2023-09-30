# C950, Brian Wong, 011147336
from package_importer import import_package
from distance_import import import_distance
from truck import Truck
from driver import Driver
from timeUtils import *
import math


# used to initially load Truck 1 and Truck 2, as well as
# when the two trucks deliver the 8 package not included
# in the initial load
def load_truck_at_hub(truck, package_hash_table, special_notes_array, early_delivery_array):
    # use the truck time in minutes for comparison logic
    truck_time_mins = truck.get_truck_time_mins()
    # change the package load time based on the current time of the loading truck
    truck_time_string = truck.get_truck_time_string()
    special_ids_to_remove = []
    for package_id in special_notes_array:
        package = package_hash_table.lookup_package(package_id)

        # add some logic to handle package id 9
        # use utils to determine if truck's current time is after 10:20AM (when address gets fixed)
        # if so, load the package
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

        # prioritize packages that must be delivered by Truck 2
        # additionally, Truck 2 will deliver the packages that have
        # the requirement of being delivered with other packages
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

                # load the current package being looked at
                truck.load_truck(package_id)
                package.update_loading_time(truck_time_string)
                package.update_status("En Route")
                package.update_delivered_by(truck.truckId)
                if package_id in early_delivery_array:
                    early_delivery_array.remove(package_id)

                # load the first package mentioned in the special notes
                if first_package_id not in truck.package_load:
                    truck.load_truck(first_package_id)
                    first_package.update_loading_time(truck_time_string)
                    first_package.update_status("En Route")
                    first_package.update_delivered_by(truck.truckId)
                    if first_package_id in early_delivery_array:
                        early_delivery_array.remove(first_package_id)

                # load the second package mentioned in the special notes
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
    # and Truck 1 will depart at 9:05 AM
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

    # Truck 2 does not go into this loop in the initial load
    # Truck 1 does so in the initial and second load
    # loading in reverse order generates a slightly better result
    # this is likely due to the fact that the packages in the beginning
    # don't share as many addresses with other packages as
    # the packages in the end
    for raw_package in reversed(package_hash_table):
        package_id = raw_package[0].id
        package = package_hash_table.lookup_package(package_id)
        if package.lookup_loading_time() == "Not Loaded Yet":
            # keep loading if the truck still has room
            # if not, start delivering
            if truck.can_load_package():
                truck.load_truck(package_id)
                package.update_loading_time(truck_time_string)
                package.update_status("En Route")
                package.update_delivered_by(truck.truckId)
            else:
                break


# nearest neighbor algorithm
def find_next_location_and_distance(truck, distance_map):
    closest_new_location = ""
    # the first location looked at will always be
    # the closest (1 of 1)
    closest_distance = float("inf")

    truck_current_location = truck.current_location
    truck_visited_locations = truck.visited_locations
    list_of_distances = distance_map[truck_current_location]
    for location, distance in list_of_distances.items():
        # not only must the location be the closest location looked at so far
        # but it must also be unvisited as omitting this requirement
        # will lead to an infinite loop of going back and forth
        # between the same 2 locations since the distance from A to B
        # is the same distance from B to A
        if location not in truck_visited_locations and distance < closest_distance:
            closest_new_location = location
            closest_distance = distance
    return closest_new_location, closest_distance


# main function that handles delivering all of the packages
# and reloading the trucks
def deliver_truck_packages(truck, distance_map, package_hash_table, special_notes_array, early_delivery_array, end_time):
    # break out of the loop once the truck has delivered
    # all of its packages and there are no more packages
    # remaining in the hub that the truck is allowed
    # to deliver (special note constraint of only Truck 2)
    while len(truck.package_load) > 0:
        hub_has_more_packages = False
        next_location, distance = find_next_location_and_distance(truck, distance_map)

        # calculate the time it will take to travel to the next location
        # if that time will push the current time pass the
        # inputted time, stop delivering
        # pushing it to the exact time is fine and desired behavior
        # round the calculated time down to ignore the truck's time in seconds
        # the user's time is in hours and seconds, so time in seconds can be disregarded
        time_to_new_location = truck.calculate_time(distance)
        new_truck_time = math.floor(truck.get_truck_time_mins() + time_to_new_location)

        if end_time is not None and new_truck_time > end_time:
            break

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

        # Truck 1 doesn't have as big of a burden as Truck 2
        # in regard to delivering packages with deadline at or
        # before 10:30 AM, so Truck 1 will deliver the 8 packages
        # that were not a part of the trucks' initial loads
        # waiting for a load of 7 led to acceptable results
        if len(truck.package_load) == 7 and truck.truckId == 1:
            for raw_package in package_hash_table:
                package_id = raw_package[0].id
                package = package_hash_table.lookup_package(package_id)
                # seeing a package has not been loaded yet is sufficient
                # information to know that there is still at least
                # one undelivered package in the hub
                if package.lookup_loading_time() == "Not Loaded Yet":
                    hub_has_more_packages = True
                    break

        # truck 2 has to go back and load the previously skipped package 3
        # this was done so that package 40 could be loaded, which has
        # a stricter deadline than package 3
        # waiting for a load of 15 meant that Truck 2 departed with its
        # initial load, delivered a package, then returned to the hub
        # to load package 3
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

            # reset the truck's visited locations as traveling back to the hub
            # will add the hub as a visited location
            # resetting after traveling will also remove the hub and cause
            # complications in the truck's traversal
            truck.reset_visited_locations()
            truck.travel_to_location(hub_address, distance_to_hub)
            load_truck_at_hub(truck, package_hash_table, special_notes_array, early_delivery_array)


def execute_simulation(user_end_time=None):
    # get assignment data
    package_hash_table, special_notes_array, early_delivery_array = import_package("package.csv")
    distance_map = import_distance("distance.csv")

    # instantiate the 3 trucks
    truck1 = Truck(1)
    truck2 = Truck(2)
    truck3 = Truck(3)

    # instantiate the 2 drivers
    driver1 = Driver("Bimmy")
    driver2 = Driver("Jimmy")

    # assign the 2 drivers to the first 2 trucks
    truck1.add_driver(driver1)
    truck2.add_driver(driver2)

    # Truck 1 will wait for the delayed packages and depart at 9:05 AM
    # waiting from 8:00 AM to 9:05 AM takes 65 minutes
    truck1.update_truck_time(65)

    # Truck 2 loads at 8:00 AM
    # Truck 1 waits until 9:05 AM then loaded
    load_truck_at_hub(truck2, package_hash_table, special_notes_array, early_delivery_array)

    # skip loading Truck 1 if the user inputs a time before 9:05 AM
    # either the user wants to see the full simulation or the user entered a time
    # don't load Truck 1 if the user input is before 9:05 AM
    truck_1_load_time = 545
    if (user_end_time is None) or (user_end_time is not None and user_end_time >= truck_1_load_time):
        load_truck_at_hub(truck1, package_hash_table, special_notes_array, early_delivery_array)

    # Truck 2 sets off first based on its load time
    deliver_truck_packages(truck2, distance_map, package_hash_table, special_notes_array, early_delivery_array, user_end_time)
    deliver_truck_packages(truck1, distance_map, package_hash_table, special_notes_array, early_delivery_array, user_end_time)

    notLoaded = 0
    package_40_string = ""
    for raw_package in package_hash_table:
        package_id = raw_package[0].id
        package = package_hash_table.lookup_package(package_id)
        if package.lookup_loading_time() == "Not Loaded Yet":
            notLoaded += 1
        if package_id == 40:
            package_40_string = (f"Package ID: {package_id} | {package.lookup_address()} |"
                                 f"Loading Time: {package.lookup_loading_time()} | "
                                 f"Delivery Time: {package.lookup_delivery_time()} | Deadline: {package.lookup_deadline()} | "
                                 f"Status: {package.lookup_delivery_status()}")
            continue
        print(
            f"Package ID: {package_id} | {package.lookup_address()} | Loading Time: {package.lookup_loading_time()} | "
            f"Delivery Time: {package.lookup_delivery_time()} | Deadline: {package.lookup_deadline()} | "
            f"Status: {package.lookup_delivery_status()}")

    print(f"Truck 1 traveled {round(truck1.get_truck_distance())} miles.")
    print(f"Truck 2 traveled {round(truck2.get_truck_distance())} miles.")
    print(f"Truck 3 traveled {round(truck3.get_truck_distance())} miles.")
    print(f"A total of "
          f"{round(truck1.get_truck_distance()) + round(truck2.get_truck_distance()) + round(truck3.get_truck_distance())} "
          f"miles were traveled.")

# facilitate console and user input
if __name__ == '__main__':
    print("--------------------")
    print("| WGUPS Simulation |")
    print("--------------------")

    # loop until the user exits
    keep_running = True
    while keep_running:
        print("\nOptions:")
        print("1. Deliver All Packages")
        print("2. View Status at a Certain Time")
        print("3. Close the Program")
        option = input("Choose an option (1, 2, or 3): ")
        if option == "1":
            execute_simulation()
        elif option == "2":
            hours = ""
            mins = ""
            am_or_pm = ""

            # get input for hours
            need_valid_hours = True
            while need_valid_hours:
                hours = int(input("Hours (1 - 12)? "))
                if hours >= 1 and hours <= 12:
                    need_valid_hours = False
                else:
                    print("Please enter a value between 1 and 12.")

            # get input for minutes
            need_valid_minutes = True
            while need_valid_minutes:
                mins = int(input("Minutes (0 - 59)? "))
                if mins >= 0 and mins <= 59:
                    need_valid_minutes = False
                else:
                    print("Please enter a value between 0 and 59.")

            need_valid_am_or_pm = True
            while need_valid_am_or_pm:
                am_or_pm = input("AM or PM? ")
                if am_or_pm == "AM" or am_or_pm == "PM":
                    need_valid_am_or_pm = False
                else:
                    print("Please choose either AM or PM.")

            # convert inputted time into time in minutes
            # for logical comparisons that check for
            # Truck 1's loading and when to stop and check status
            user_time_string = f"{hours}:{mins} {am_or_pm}"
            user_time_mins = time_string_to_mins((user_time_string))

            # reformat the string so minutes have a leading 0 when appropriate
            formatted_time_string = mins_to_time_string(user_time_mins)

            print(f"Checking status at {formatted_time_string}.")
            execute_simulation(user_time_mins)
        elif option == "3":
            keep_running = False
        else:
            print("That is not a valid option, please try again.")
