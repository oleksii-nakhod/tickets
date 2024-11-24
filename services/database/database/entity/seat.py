from .base import *

class Seat(Base):
    __tablename__ = "seat"

    id: Mapped[int] = mapped_column(primary_key=True)
    num: Mapped[int] = mapped_column()
    carriage_id: Mapped[int] = mapped_column(ForeignKey("carriage.id"))
    carriage: Mapped["Carriage"] = relationship(back_populates="seat")
    ticket: Mapped[List["Ticket"]] = relationship(back_populates="seat")

    def __repr__(self) -> str:
        return f"Seat(id={self.id!r}, num={self.num!r}, carriage_id={self.carriage_id!r})"
    
    def to_dict(self):
        return {
            'id': self.id,
            'num': self.num,
            'carriage_id': self.carriage_id
        }