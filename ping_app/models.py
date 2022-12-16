from datetime import datetime

from sqlalchemy import String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    is_online: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())


class Host(Base):
    __tablename__ = "host"

    address: Mapped[str] = mapped_column(String, unique=True)
    zone: Mapped[int] = mapped_column(ForeignKey("zone.id"))

    zone_group: Mapped["Zone"] = relationship(back_populates="addresses")

    def __repr__(self):
        return f"{self.name} - {self.zone_group}"


class Zone(Base):
    __tablename__ = "zone"

    addresses: Mapped[list["Host"]] = relationship(back_populates="zone_group", cascade="all, delete-orphan")

    def __repr__(self):
        return f"{self.name} - {self.is_online}"
