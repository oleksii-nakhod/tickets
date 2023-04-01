class TripStation():
    def __init__(self, id, trip_id, station_id, num, time_arr, time_dep, price):
        self.id = id
        self.trip_id = trip_id
        self.station_id = station_id
        self.num = num
        self.time_arr = time_arr
        self.time_dep = time_dep
        self.price = price

    def print_info(self):
        print(f'Trip Station #{self.id}\nTrip ID: {self.trip_id}\nStation ID: {self.station_id}\nNum: {self.num}\nArrival Time: {self.time_arr}\nDeparture Time: {self.time_dep}\n')
