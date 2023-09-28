import csv
from hash_table import HashTable
from package import Package


def import_package(package_file):
    hash_table = HashTable()
    special_notes_array = []
    early_delivery_array = []

    with open(package_file, encoding='utf-8-sig') as packages:
        reader = csv.reader(packages, delimiter=",")
        # skip the header row
        next(reader)
        for row in reader:
            package_id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zip = row[4]
            deadline = row[5]
            weight = int(row[6])
            notes = row[7]
            package = Package(package_id, address, city, state, zip, deadline, weight, notes)
            hash_table.insert_package(package_id, package)

            if notes != "":
                special_notes_array.append(package_id)
            elif deadline == "9:00 AM" or deadline == "10:30 AM":
                early_delivery_array.append(package_id)
    # for i in range(0, 40):
    #     package = hash_table.lookup_package(i)
    #     id = package.lookup_id()
    #     address = package.lookup_address()
    #     city = package.lookup_city()
    #     state = package.lookup_state()
    #     zip = package.lookup_zip()
    #     deadline = package.lookup_deadline()
    #     weight = package.lookup_weight()
    #     notes = package.lookup_notes()
    #     status = package.lookup_delivery_status()
    #     time = package.lookup_delivery_time()
    #     print([id, address, city, state, zip, deadline, weight, notes, status, time])
    return [hash_table, special_notes_array, early_delivery_array]
