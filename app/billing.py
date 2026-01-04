from sqlalchemy.orm import Session

from .models import Room, MeterReading, Bill, PriceConfig

def get_latest_price(db: Session) -> PriceConfig:
    pc = db.query(PriceConfig).order_by(PriceConfig.effective_from.desc()).first()
    if not pc:
        pc = PriceConfig(water_price=4.0, elec_price=0.8, gas_price=3.0, property_rate=0.5)
        db.add(pc)
        db.commit()
        db.refresh(pc)
    return pc

def get_last_reading_before(db: Session, room_id: int, period: str):
    return (
        db.query(MeterReading)
        .filter(MeterReading.room_id == room_id, MeterReading.period < period)
        .order_by(MeterReading.period.desc())
        .first()
    )

def generate_bill_for_room(db: Session, room: Room, period: str) -> Bill:
    reading_now = (
        db.query(MeterReading)
        .filter(MeterReading.room_id == room.id, MeterReading.period == period)
        .first()
    )
    if not reading_now:
        raise ValueError(f"房间 {room.room_no} 在 {period} 没有抄表记录")

    last = get_last_reading_before(db, room.id, period)
    if last:
        water_prev, elec_prev, gas_prev = last.water, last.elec, last.gas
    else:
        water_prev, elec_prev, gas_prev = room.water_base, room.elec_base, room.gas_base

    water_used = reading_now.water - water_prev
    elec_used = reading_now.elec - elec_prev
    gas_used = reading_now.gas - gas_prev

    pc = get_latest_price(db)

    water_fee = water_used * pc.water_price
    elec_fee = elec_used * pc.elec_price
    gas_fee = gas_used * pc.gas_price

    # 物业费：当月实际用电量 × 物业单价（默认 0.5）
    property_fee = elec_used * pc.property_rate

    total = room.base_rent + water_fee + elec_fee + gas_fee + property_fee

    bill = (
        db.query(Bill)
        .filter(Bill.room_id == room.id, Bill.period == period)
        .first()
    )
    if not bill:
        bill = Bill(room_id=room.id, period=period)

    bill.rent_fee = room.base_rent
    bill.water_used, bill.elec_used, bill.gas_used = water_used, elec_used, gas_used
    bill.water_fee, bill.elec_fee, bill.gas_fee = water_fee, elec_fee, gas_fee
    bill.property_rate = pc.property_rate
    bill.property_fee = property_fee
    bill.total = total

    db.add(bill)
    db.commit()
    db.refresh(bill)
    return bill
