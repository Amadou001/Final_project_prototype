#!/usr/bin/python3
"""property module"""
from models.base_model import BaseModel, Base
from sqlalchemy import Integer, String, Column, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.transaction import Transaction
from models.whishlist import Whishlist
from models.message import Message
from models.review import Review
import os

class Property(BaseModel, Base):
    """Mapping class for property table"""

    __tablename__ = "property"
    title = Column(String(50), nullable=False)
    description = Column(String(2050), nullable=False)
    property_type = Column(String(10), nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String(10), nullable=True)
    listing_type = Column(String(5), nullable=False)
    address = Column(String(224), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)
    zip_code = Column(String(15), nullable=True)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    area = Column(Float, nullable=False)
    user_id = Column(String(60), ForeignKey('user.id'), nullable=False)

    user = relationship("User", back_populates="properties")
    transaction = relationship("Transaction", back_populates="property1", cascade="all, delete-orphan")
    property_image = relationship("Property_image", back_populates="property2", cascade="all, delete-orphan")
    whishlists = relationship("Whishlist", back_populates="properties")
    messages = relationship("Message", back_populates="property3")
    reviews = relationship("Review", back_populates="property")
