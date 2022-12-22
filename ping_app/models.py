
from datetime import datetime

from sqlalchemy import String, Boolean, ForeignKey, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class Host(Base):
    __tablename__ = "host"

    name: Mapped[str]
    is_online: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    address: Mapped[str] = mapped_column(String, unique=True)
    zone: Mapped[int] = mapped_column(ForeignKey("zone.id"))

    zone_group: Mapped["Zone"] = relationship(back_populates="addresses")

    def __repr__(self):
        return f"{self.name} - {self.zone_group}"


class Zone(Base):
    __tablename__ = "zone"

    name: Mapped[str]
    is_online: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    addresses: Mapped[list["Host"]] = relationship(back_populates="zone_group", cascade="all, delete-orphan")
    periods: Mapped[list["Period"]] = relationship(back_populates="zone_group", cascade="all, delete-orphan")
    subscribers: Mapped[list["Subscription"]] = relationship(back_populates="zone_group", cascade="all, delete-orphan")

    def __repr__(self):
        return f"{self.name} - {self.is_online}"


class Period(Base):
    __tablename__ = "period"

    zone: Mapped[int] = mapped_column(ForeignKey("zone.id"))
    is_online: Mapped[bool] = mapped_column(Boolean, default=False)
    start: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    end: Mapped[datetime] = mapped_column(DateTime)
    duration: Mapped[int]

    zone_group: Mapped["Zone"] = relationship(back_populates="periods")


class User(Base):
    __tablename__ = "user"

    name: Mapped[str]
    subscriptions: Mapped[list["Subscription"]] = relationship(back_populates="subscribers")


    def __repr__(self):
        return f"{self.name}"


class Subscription(Base):
    __tablename__ = "subscription"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    zone_id: Mapped[int] = mapped_column(ForeignKey("zone.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    zone_group: Mapped["Zone"] = relationship(back_populates="subscribers")
    subscribers: Mapped[list["User"]] = relationship(back_populates="subscriptions")
