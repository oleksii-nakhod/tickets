from .base import *

class TripStation(Base):
    __tablename__ = "trip_station"

    id: Mapped[int] = mapped_column(primary_key=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trip.id"))
    trip: Mapped["Trip"] = relationship(back_populates="trip_station")
    station_id: Mapped[int] = mapped_column(ForeignKey("station.id"))
    station: Mapped["Station"] = relationship(back_populates="trip_station")
    num: Mapped[int] = mapped_column()
    time_arr: Mapped[datetime.datetime] = mapped_column()
    time_dep: Mapped[datetime.datetime] = mapped_column()
    price: Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"TripStation(id={self.id!r}, trip_id={self.trip_id!r}, station_id={self.station_id!r}, num={self.num!r}, time_arr={self.time_arr!r}, time_dep={self.time_dep!r}, price={self.price!r})"
    
    def to_dict(self):
        return {
            'id': self.id,
            'trip_id': self.trip_id,
            'station_id': self.station_id,
            'num': self.num,
            'time_arr': self.time_arr.isoformat() + 'Z',
            'time_dep': self.time_dep.isoformat() + 'Z',
            'price': self.price
        }