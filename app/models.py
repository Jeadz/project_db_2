from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, index=True)
    email = Column(String, index=True)

class Dish(Base):
    __tablename__ = "dishes"
    id = Column(Integer, primary_key=True, index=True)
    dish_name = Column(String, index=True)
    price = Column(Float, index=True)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("users.id"))
    order_date = Column(Date, index=True)
    user = relationship("User")

class RestaurantTable(Base):
    __tablename__ = "restaurant_tables"
    id = Column(Integer, primary_key=True, index=True)
    table_number = Column(Integer, index=True)
    capacity = Column(Integer, index=True)

class Booking(Base):
    __tablename__ = "booking"
    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("users.id"))
    id_table = Column(Integer, ForeignKey("restaurant_tables.id"))
    booking_date = Column(Date, index=True)
    user = relationship("User")
    table = relationship("RestaurantTable")

class DishOrders(Base):
    __tablename__ = "dish_orders"
    id = Column(Integer, primary_key=True, index=True)
    id_order = Column(Integer, ForeignKey("orders.id"))
    id_dish = Column(Integer, ForeignKey("dishes.id"))
    amount = Column(Integer, index=True)
    order = relationship("Order")
    dish = relationship("Dish")
