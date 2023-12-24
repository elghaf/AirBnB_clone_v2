#!/usr/bin/python3
"""The definition of Amenity class for this project."""
from models.base_model import Base
from models.base_model import BaseModel
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Representation of the Amenity for a MySQL database in this project.
    Getteing from SQLAlchemy Base  to the MySQL table amenities.
    Attributes:
        __tablename__ (str): The MySQL table name  to save Amenities.
        name (sqlalchemy String): The amenity nomination
        place_amenities (sqlalchemy relationship): Relationship between Place-Amenity.
    """
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary="place_amenity",
                                   viewonly=False)
