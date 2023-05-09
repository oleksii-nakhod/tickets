from .base import *

class CarriageType(Base):
    __tablename__ = "carriage_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    price_mod: Mapped[int] = mapped_column()
    carriage: Mapped[List["Carriage"]] = relationship(back_populates="carriage_type")

    def __repr__(self) -> str:
        return f"CarriageType(id={self.id!r}, name={self.name!r}, price_mod={self.price_mod!r})"