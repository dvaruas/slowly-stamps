from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing_extensions import Annotated

str_10 = Annotated[str, 10]
str_150 = Annotated[str, 150]


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

used_stamps = Table(
    "used_stamps",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE")),
    Column("stamp_id", ForeignKey("stamps.id", ondelete="CASCADE")),
)


class Users(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement="auto",
    )
    name: Mapped[str_150] = mapped_column(
        String(150),
        nullable=False,
    )
    image_id: Mapped[str_10] = mapped_column(
        String(10),
        unique=True,
        nullable=True,
    )
    used_stamps: Mapped[List["Stamps"]] = relationship(
        secondary=used_stamps,
    )


class StampCategories(db.Model):
    __tablename__ = "stamp_categories"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement="auto",
    )
    name: Mapped[str_150] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )
    stamps: Mapped[List["Stamps"]] = relationship()


class Stamps(db.Model):
    __tablename__ = "stamps"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement="auto",
    )
    name: Mapped[str_150] = mapped_column(
        String(150),
        nullable=False,
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey(
            "stamp_categories.id",
            ondelete="CASCADE",
        ),
    )
    image_id: Mapped[str_10] = mapped_column(
        String(10),
        nullable=True,
        unique=True,
    )
