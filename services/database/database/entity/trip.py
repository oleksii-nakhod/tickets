from .base import *

class Trip(Base):
    __tablename__ = "trip"

    id: Mapped[int] = mapped_column(primary_key=True)
    train_id: Mapped[int] = mapped_column(ForeignKey("train.id"))
    train: Mapped["Train"] = relationship(back_populates="trip")
    trip_station: Mapped[List["TripStation"]] = relationship(back_populates="trip")

    def __repr__(self) -> str:
        return f"Trip(id={self.id!r}, train_id={self.train_id!r})"
    
    def to_dict(self):
        return {
            'id': self.id,
            'train_id': self.train_id
        }