from .base import *

class Train(Base):
    __tablename__ = "train"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    carriage: Mapped[List["Carriage"]] = relationship(back_populates="train")
    trip: Mapped[List["Trip"]] = relationship(back_populates="train")

    def __repr__(self) -> str:
        return f"Train(id={self.id!r}, name={self.name!r})"
