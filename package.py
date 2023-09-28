class Package:
    def __init__(self, id, address, city, state, zip, deadline, weight, notes, delivery_status="At Hub",
                 loading_time="Not Loaded Yet", delivery_time="Not Delivered Yet"):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.delivery_status = delivery_status
        self.loading_time = loading_time
        self.delivery_time = delivery_time
        self.delivered_by = ""

    def update_address(self, new_address):
        self.address = new_address

    def update_status(self, new_status):
        self.delivery_status = new_status

    def update_loading_time(self, new_loading_time):
        self.loading_time = new_loading_time

    def update_delivery_time(self, new_delivery_time):
        self.delivery_time = new_delivery_time

    def update_delivered_by(self, truck_id):
        self.delivered_by = truck_id

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
        return self.delivery_status

    def lookup_loading_time(self):
        return self.loading_time

    def lookup_delivery_time(self):
        return self.delivery_time

    def lookup_delivered_by(self):
        return f"Delivered By Truck {self.delivered_by}"
