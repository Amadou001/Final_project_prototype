#!/usr/bin/python3
"""Message module"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import os


class Message(BaseModel, Base):
    """Mapping class for message table"""

    __tablename__ = "message"

    message_content = Column(String(1024), nullable=True)
    read_status = Column(String(10), nullable=True)
    property_id = Column(String(60), ForeignKey('property.id'), nullable=False)
    sender_id = Column(String(60), ForeignKey('user.id'), nullable=False)
    receiver_id = Column(String(60), ForeignKey('user.id'), nullable=False)

    property3 = relationship("Property", back_populates="messages")
    sender = relationship("User", foreign_keys=[sender_id], back_populates="messages1")
    receiver = relationship("User", foreign_keys=[receiver_id],  back_populates="messages2")
