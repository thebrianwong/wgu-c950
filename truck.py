from timeUtils import *


class Truck:
    def __init__(self, id, max_capacity=16, speed=18):
        self.truckId = id
        self.driver = None
        self.max_capacity = max_capacity
        self.speed = speed
        self.package_load = []
        self.current_location = "4001 South 700 East"
        self.visited_locations = ["4001 South 700 East"]
        # number of minutes at 8:00 AM
        self.current_time = 480
        self.distance = 0

    def has_driver(self):
        return True if self.driver is not None else False

    def add_driver(self, driver):
        self.driver = driver

    def can_load_package(self):
        return len(self.package_load) < self.max_capacity

    def load_truck(self, id):
        if not self.can_load_package():
            print(f"Truck No. {self.truckId} can't fit any more packages!!! Unable to add package {id}")
            return False
        self.package_load.append(id)

    def get_truck_time_mins(self):
        return self.current_time

    def get_truck_time_string(self):
        return mins_to_time_string(round(self.current_time))

    def update_truck_time(self, added_time):
        self.current_time += added_time

    def get_truck_distance(self):
        return self.distance

    def update_truck_distance(self, added_distance):
        self.distance += added_distance

    def calculate_time(self, distance):
        time = distance / self.speed * 60
        return time

    def travel_to_location(self, location_name, traveled_distance):
        travel_time = self.calculate_time(traveled_distance)
        self.update_truck_time(travel_time)
        self.update_truck_distance(traveled_distance)
        self.current_location = location_name
        self.visited_locations.append(location_name)

    def reset_visited_locations(self):
        self.visited_locations = []
