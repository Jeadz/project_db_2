from pydantic import BaseModel
from typing import List

class UserBase(BaseModel):
    fullname: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class DishBase(BaseModel):
    dish_name: str
    price: float

class DishCreate(DishBase):
    pass

class Dish(DishBase):
    id: int
    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    id_user: int
    order_date: str

class OrderCreate(OrderBase):
    pass
class Order(OrderBase):
    id: int
    class Config:
        orm_mode = True
class TableBase(BaseModel):
    table_number: int
    capacity: int

class TableCreate(TableBase):
    pass

class Table(TableBase):
    id: int
    class Config:
        orm_mode = True

class BookingBase(BaseModel):
    id_user: int
    id_table: int
    booking_date: str

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    class Config:
        orm_mode = True

class DishOrdersBase(BaseModel):
    id_order: int
    id_dish: int
    amount: int

class DishOrdersCreate(DishOrdersBase):
    pass

class DishOrderss(DishOrdersBase):
    id: int
    class Config:
        orm_mode = True
