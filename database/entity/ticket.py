class Ticket():
    def __init__(self, id, user_id, seat_id, trip_station_start_id, trip_station_end_id):
        self.id = id
        self.user_id = user_id
        self.seat_id = seat_id
        self.trip_station_start_id = trip_station_start_id
        self.trip_station_end_id = trip_station_end_id

    def print_info(self):
        print(f'Ticket #{self.id}\nUser ID: {self.user_id}\nSeat ID: {self.seat_id}\nTrip Station Start ID: {self.trip_station_start_id}\nTrip Station End ID: {self.trip_station_end_id}\n')
