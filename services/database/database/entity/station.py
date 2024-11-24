from .base import *

class Station(Base):
    __tablename__ = "station"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    trip_station: Mapped[List["TripStation"]] = relationship(back_populates="station")

    def __repr__(self) -> str:
        return f"Station(id={self.id!r}, name={self.name!r})"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }