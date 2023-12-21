#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import os
from models.city import City


class State(BaseModel, Base):
    """State class"""
    __tablename__ = 'states'

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship('City', cascade='all, delete, delete-orphan', backref='state')
    else:
        name = ""

        @property
        def cities(self):
            """Returns the cities in this State"""
            from models import storage
            return [value for value in storage.all(City).values() if value.state_id == self.id]

