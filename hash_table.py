class HashTable:
    def __init__(self, buckets=40):
        self.hash_table = []
        for i in range(buckets):
            self.hash_table.append([])

    def _calculate_bucket(self, id):
        bucket_num = id % len(self.hash_table)
        bucket = self.hash_table[bucket_num]
        return bucket

    def insert_package(self, id, package):
        bucket = self._calculate_bucket(id)
        bucket.append(package)

    def lookup_package(self, id):
        bucket = self._calculate_bucket(id)
        package = bucket[0]
        return package
