from __future__ import annotations
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    addresses: Mapped[List["Address"]] = relationship(
        "Address",
        back_populates="user",
        foreign_keys="Address.user_id",
    )

class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email_address: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_account.id", ondelete="CASCADE"), index=True
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="addresses",
        foreign_keys=[user_id],
    )

def main(argv=None):
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

    Base.metadata.create_all(engine)

if __name__ == "__main__":
    main()