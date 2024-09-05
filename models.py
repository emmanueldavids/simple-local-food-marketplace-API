from database import Base
from datetime import date

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash



Base = declarative_base()


class Farmer(Base):
    __tablename__ = 'farmers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    password = Column(String(128))
    farm_name = Column(String(100))
    location = Column(String(100))

    products = relationship('Product', backref='farmers')
    reviews = relationship('Review', backref='farmers')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(String(200))
    price = Column(Float)
    category = Column(String(50))
    farmer_id = Column(Integer, ForeignKey('farmers.id'))

    orders = relationship('Order', backref='products')
    reviews = relationship('Review', backref='products')


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    total = Column(Float)
    status = Column(String(50))

    customer = relationship('Customer', backref='order')
    product = relationship('Product', backref='order')


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    username = Column(String(100), unique=True)
    email = Column(String(100), unique=True)
    password = Column(String(128))

    orders = relationship('Order', backref='customers')
    reviews = relationship('Review', backref='customers')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    farmer_id = Column(Integer, ForeignKey('farmers.id'))
    rating = Column(Integer)
    comment = Column(String(200))

    
    customer = relationship('Customer', backref='review')
    product = relationship('Product', backref='review')
    farmer = relationship('Farmer', backref='review')