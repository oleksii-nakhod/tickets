from .base import *

class UserRole(Base):
    __tablename__ = "user_role"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    user: Mapped[List["User"]] = relationship(back_populates="user_role")

    def __repr__(self) -> str:
        return f"UserRole(id={self.id!r}, name={self.name!r})"
