class HashTable:
    def __int__(self, buckets=40):
        self.hash_table = []
        for i in range(buckets):
            self.hash_table.append([None, None, None, None, None, None, None, None])

    def _calculate_bucket(self, id):
        bucket_num = id % len(self.hash_table)
        bucket = self.hash_table[bucket_num]
        return bucket
    def insert_address(self, id, address):
        bucket = self._calculate_bucket(id)
        bucket[0] = address

    def insert_city(self, id, city):
        bucket = self._calculate_bucket(id)
        bucket[1] = city

    def insert_state(self, id, state):
        bucket = self._calculate_bucket(id)
        bucket[2] = state

    def insert_zip(self,id, zip):
        bucket = self._calculate_bucket(id)
        bucket[3] = zip

    def insert_deadline(self, id, deadline):
        bucket = self._calculate_bucket(id)
        bucket[4] = deadline

    def insert_weight(self, id, weight):
        bucket = self._calculate_bucket(id)
        bucket[5] = weight

    def insert_notes(self, id, notes):
        bucket = self._calculate_bucket(id)
        bucket[6] = notes

    def insert_status(self, id, status):
        bucket = self._calculate_bucket(id)
        bucket[7] = status

    def get_address(self, id):
        bucket = self._calculate_bucket(id)
        address = bucket[0]
        return address

    def get_city(self, id):
        bucket = self._calculate_bucket(id)
        city = bucket[1]
        return city

    def get_state(self, id):
        bucket = self._calculate_bucket(id)
        state = bucket[2]
        return state

    def get_zip(self, id):
        bucket = self._calculate_bucket(id)
        zip = bucket[3]
        return zip

    def get_deadline(self, id):
        bucket = self._calculate_bucket(id)
        deadline = bucket[4]
        return deadline

    def get_weight(self, id):
        bucket = self._calculate_bucket(id)
        weight = bucket[5]
        return weight

    def get_notes(self, id):
        bucket = self._calculate_bucket(id)
        notes = bucket[6]
        return notes

    def get_status(self, id):
        bucket = self._calculate_bucket(id)
        status = bucket[7]
        return status
