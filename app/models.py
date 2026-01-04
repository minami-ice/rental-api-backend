from __future__ import annotations

from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="user")  # admin / user
    is_active: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    room_no: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    base_rent: Mapped[float] = mapped_column(Float, default=0.0)
    water_base: Mapped[float] = mapped_column(Float, default=0.0)
    elec_base: Mapped[float] = mapped_column(Float, default=0.0)
    gas_base: Mapped[float] = mapped_column(Float, default=0.0)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    readings = relationship("MeterReading", back_populates="room", cascade="all, delete-orphan")
    bills = relationship("Bill", back_populates="room", cascade="all, delete-orphan")

class MeterReading(Base):
    __tablename__ = "meter_readings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"), index=True)
    period: Mapped[str] = mapped_column(String(7), index=True)  # YYYY-MM

    water: Mapped[float] = mapped_column(Float, default=0.0)
    elec: Mapped[float] = mapped_column(Float, default=0.0)
    gas: Mapped[float] = mapped_column(Float, default=0.0)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    room = relationship("Room", back_populates="readings")

    __table_args__ = (UniqueConstraint("room_id", "period", name="uq_room_period_reading"),)

class PriceConfig(Base):
    __tablename__ = "price_config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    water_price: Mapped[float] = mapped_column(Float, default=4.0)
    elec_price: Mapped[float] = mapped_column(Float, default=0.8)
    gas_price: Mapped[float] = mapped_column(Float, default=3.0)

    # 物业费单价（元/度），默认 0.5
    property_rate: Mapped[float] = mapped_column(Float, default=0.5)

    effective_from: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

class Bill(Base):
    __tablename__ = "bills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"), index=True)
    period: Mapped[str] = mapped_column(String(7), index=True)  # YYYY-MM

    rent_fee: Mapped[float] = mapped_column(Float, default=0.0)

    water_used: Mapped[float] = mapped_column(Float, default=0.0)
    elec_used: Mapped[float] = mapped_column(Float, default=0.0)
    gas_used: Mapped[float] = mapped_column(Float, default=0.0)

    water_fee: Mapped[float] = mapped_column(Float, default=0.0)
    elec_fee: Mapped[float] = mapped_column(Float, default=0.0)
    gas_fee: Mapped[float] = mapped_column(Float, default=0.0)

    property_rate: Mapped[float] = mapped_column(Float, default=0.5)
    property_fee: Mapped[float] = mapped_column(Float, default=0.0)

    total: Mapped[float] = mapped_column(Float, default=0.0)

    # 收款状态
    is_paid: Mapped[int] = mapped_column(Integer, default=0)  # 0未收 1已收
    paid_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    pay_method: Mapped[str | None] = mapped_column(String(30), nullable=True)
    remark: Mapped[str | None] = mapped_column(String(200), nullable=True)

    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    room = relationship("Room", back_populates="bills")

    __table_args__ = (UniqueConstraint("room_id", "period", name="uq_room_period_bill"),)
