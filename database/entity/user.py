from .base import *

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30))
    password_hash: Mapped[str] = mapped_column(String(60))
    user_role_id: Mapped[int] = mapped_column(ForeignKey("user_role.id"))
    user_role: Mapped["UserRole"] = relationship(back_populates="user")
    ticket: Mapped[List["Ticket"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"