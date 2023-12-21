#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import os


class City(BaseModel, Base):
    """The city class, contains state ID and name"""
    __tablename__ = 'cities'

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = relationship(
            'Place',
            cascade='all, delete, delete-orphan',
            backref='city'
        )
    else:
        name = ""
        state_id = ""
        places = None