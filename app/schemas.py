from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional, List

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    username: str
    role: str
    is_active: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=6, max_length=100)
    role: str = Field(default="user")  # admin/user

class RoomIn(BaseModel):
    room_no: str
    base_rent: float = 0.0
    water_base: float = 0.0
    elec_base: float = 0.0
    gas_base: float = 0.0

class RoomOut(RoomIn):
    id: int

    class Config:
        from_attributes = True

class ReadingIn(BaseModel):
    room_id: int
    period: str  # YYYY-MM
    water: float
    elec: float
    gas: float

class ReadingOut(ReadingIn):
    id: int

    class Config:
        from_attributes = True

class PriceIn(BaseModel):
    water_price: float
    elec_price: float
    gas_price: float
    property_rate: float = 0.5

class PriceOut(PriceIn):
    id: int
    effective_from: str

    class Config:
        from_attributes = True

class PayUpdateIn(BaseModel):
    is_paid: int  # 0/1
    paid_at: Optional[str] = None  # "YYYY-MM-DD HH:MM:SS" 或 None
    pay_method: Optional[str] = None
    remark: Optional[str] = None

class PayBatchUpdateIn(BaseModel):
    bill_ids: List[int]
    is_paid: int
    paid_at: Optional[str] = None
    pay_method: Optional[str] = None
    remark: Optional[str] = None

class BillOut(BaseModel):
    id: int
    room_id: int
    room_no: str
    period: str

    rent_fee: float

    water_used: float
    elec_used: float
    gas_used: float

    water_fee: float
    elec_fee: float
    gas_fee: float

    property_rate: float
    property_fee: float

    total: float

    is_paid: int
    paid_at: Optional[str] = None
    pay_method: Optional[str] = None
    remark: Optional[str] = None

    class Config:
        from_attributes = True
