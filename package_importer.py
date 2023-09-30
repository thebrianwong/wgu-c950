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

    return [hash_table, special_notes_array, early_delivery_array]
