from .base import *

class Carriage(Base):
    __tablename__ = "carriage"

    id: Mapped[int] = mapped_column(primary_key=True)
    num: Mapped[int] = mapped_column()
    train_id: Mapped[int] = mapped_column(ForeignKey("train.id"))
    train: Mapped["Train"] = relationship(back_populates="carriage")
    carriage_type_id: Mapped[int] = mapped_column(ForeignKey("carriage_type.id"))
    carriage_type: Mapped["CarriageType"] = relationship(back_populates="carriage")
    seat: Mapped[List["Seat"]] = relationship(back_populates="carriage")

    def __repr__(self) -> str:
        return f"Carriage(id={self.id!r}, num={self.num!r}, train_id={self.train_id!r}, carriage_type_id={self.carriage_type_id!r})"