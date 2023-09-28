import csv

def import_distance(distance_file):
    distance_map = {}
    with open(distance_file, encoding='utf-8-sig') as distances:
        reader = csv.reader(distances, delimiter=",")
        headers = next(reader)
        for row in reader:
            row_data = {}
            for i, val in enumerate(row):
                row_data[headers[i]] = float(val)
            for header in headers:
                if header not in distance_map:
                    distance_map[header] = row_data
                    break
    return distance_map
