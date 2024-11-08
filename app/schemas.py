from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class UserBase(BaseModel):
    fullname: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    fullname: Optional[str] = None
    email: Optional[str] = None
    
class DishBase(BaseModel):
    dish_name: str
    price: float

class DishCreate(DishBase):
    pass

class Dish(DishBase):
    id: int
    class Config:
        orm_mode = True

class DishUpdate(BaseModel):
    dish_name: Optional[str] = None
    price: Optional[float] = None
    
class OrderBase(BaseModel):
    id_user: int
    order_date: date
    
class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    class Config:
        orm_mode = True
        
class OrderUpdate(BaseModel):
    id_user: Optional[int] = None
    order_date: Optional[date] = None

class TableBase(BaseModel):
    table_number: int
    capacity: int

class TableCreate(TableBase):
    pass

class Table(TableBase):
    id: int
    class Config:
        orm_mode = True
        
class TableUpdate(BaseModel):
    table_number: Optional[int] = None  
    capacity: Optional[int] = None

class BookingBase(BaseModel):
    id_user: int
    id_table: int
    booking_date: date
    
class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    class Config:
        orm_mode = True
        
class BookingUpdate(BaseModel):
    id_user: Optional[int] = None
    id_table: Optional[int] = None
    booking_date: Optional[date] = None
        
class DishOrdersBase(BaseModel):
    id_order: int
    id_dish: int
    amount: int
    
class DishOrdersCreate(DishOrdersBase):
    pass

class DishOrders(DishOrdersBase):
    id: int
    class Config:
        orm_mode = True

class DishOrdersUpdate(BaseModel):
    id_order: Optional[int] = None
    id_dish: Optional[int] = None
    amount: Optional[int] = None