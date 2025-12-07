from typing import Annotated
from datetime import datetime
import enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Numeric, ForeignKey, BigInteger, TIMESTAMP, text

from database.database import Base


intpk = Annotated[int, mapped_column(primary_key=True)]


class Categories(Base):
    __tablename__ = "categories"
    
    id: Mapped[intpk]
    category_name: Mapped[str] = mapped_column(String(50))
    is_active: Mapped[bool]

    teas: Mapped[list["Teas"]] = relationship(back_populates="category") #relationship


class Teas(Base):
    __tablename__ = "teas"

    id: Mapped[intpk]
    tea_name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str]
    price: Mapped[float] = mapped_column(Numeric(scale=3))
    stock: Mapped[int]
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped[list["Categories"]] = relationship(back_populates="teas") #relationship   
    image_url: Mapped[str]
    is_active: Mapped[bool]


class Users(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    user_name: Mapped[str] = mapped_column(String(32))
    full_name: Mapped[str] = mapped_column(String(70))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()")
    )


class Admins(Base):
    __tablename__ = "admins"
    id: Mapped[intpk]
    admin_tg_id: Mapped[int] = mapped_column(BigInteger)


class Cart(Base):
    __tablename__ = "cart"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    tea_id: Mapped[int] = mapped_column(ForeignKey("teas.id"))
    quantity: Mapped[int] = mapped_column(BigInteger)


#Статусы для заказов
class Status(enum.Enum):
    await_pay = "await_pay"
    paid = "paid"
    deliver = "deliver"
    on_way = "on_way"
    wait_receipt = "wait_receipt"


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(70))
    label: Mapped[str] = mapped_column(String(70))
    total_price: Mapped[float] = mapped_column(Numeric(scale=3))
    user_name: Mapped[str] = mapped_column(String(30))
    address: Mapped[str] = mapped_column(String(80))
    phone: Mapped[str] = mapped_column(String(12))