from .base import *

class Ticket(Base):
    __tablename__ = "ticket"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="ticket")
    seat_id: Mapped[int] = mapped_column(ForeignKey("seat.id"))
    seat: Mapped["Seat"] = relationship(back_populates="ticket")
    trip_station_start_id: Mapped[int] = mapped_column(ForeignKey("trip_station.id"))
    trip_station_start: Mapped["TripStation"] = relationship(foreign_keys=[trip_station_start_id])
    trip_station_end_id: Mapped[int] = mapped_column(ForeignKey("trip_station.id"))
    trip_station_end: Mapped["TripStation"] = relationship(foreign_keys=[trip_station_end_id])
    token: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f"Ticket(id={self.id!r}, user_id={self.user_id!r}, seat_id={self.seat_id!r}, trip_station_start_id={self.trip_station_start_id!r}, trip_station_end_id={self.trip_station_end_id!r}, token={self.token!r})"
