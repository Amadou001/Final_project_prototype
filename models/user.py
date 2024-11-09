#!/usr/bin/python3
"""User module"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.property import Property
from models.transaction import Transaction
from models.whishlist import Whishlist
from models.message import Message
from models.review import Review
import os

class User(BaseModel, Base):
    """Mapping class for user table"""
    __tablename__ = "user"
    first_name = Column(String(224), nullable=False)
    last_name = Column(String(224), nullable=False)
    email = Column(String(224), nullable=True)
    phone_number = Column(String(45), nullable=True)
    password = Column(String(45), nullable=True)
    user_type = Column(String(10), nullable=True)
    profile_image = Column(String(65), nullable=True)

    properties = relationship("Property", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    whishlists = relationship("Whishlist", back_populates="user", cascade="all, delete-orphan")
    messages1 = relationship("Message", foreign_keys="[Message.sender_id]", back_populates="sender", cascade="all, delete-orphan")
    messages2 = relationship("Message", foreign_keys="[Message.receiver_id]", back_populates="receiver", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")

