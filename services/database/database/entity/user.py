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
    confirmed_email: Mapped[bool] = mapped_column()
    confirm_email_token: Mapped[str] = mapped_column()
    reset_password_token: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password_hash': self.password_hash,
            'user_role_id': self.user_role_id,
            'confirmed_email': self.confirmed_email,
            'confirm_email_token': self.confirm_email_token,
            'reset_password_token': self.reset_password_token
        }