class Package:
    def __init__(self, id, address, city, state, zip, deadline, weight, notes, deliveryStatus="At Hub",
                 deliveryTime="Not Delivered Yet"):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.deliveryStatus = deliveryStatus
        self.deliveryTime = deliveryTime

    def update_address(self, newAddress):
        self.address = newAddress

    def update_status(self, newStatus):
        self.deliveryStatus = newStatus

    def update_time(self, newTime):
        self.deliveryTime = newTime

    def lookup_id(self):
        return self.id

    def lookup_address(self):
        return self.address

    def lookup_city(self):
        return self.city

    def lookup_state(self):
        return self.state

    def lookup_zip(self):
        return self.zip

    def lookup_deadline(self):
        return self.deadline

    def lookup_weight(self):
        return self.weight

    def lookup_notes(self):
        return self.notes

    def lookup_delivery_status(self):
        return self.deliveryStatus

    def lookup_delivery_time(self):
        return self.deliveryTime
