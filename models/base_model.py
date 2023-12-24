#!/usr/bin/python3
"""Defines the BaseModel class."""
from datetime import datetime
from uuid import uuid4
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DATETIME

Base = declarative_base()


class BaseModel:
    """Represents the BaseModel of the HBnB project."""

    id = Column(String(60),
                nullable=False,
                primary_key=True,
                unique=True)
    created_at = Column(DATETIME,
                        nullable=False,
                        default=datetime.utcnow())
    updated_at = Column(DATETIME,
                        nullable=False,
                        default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the BaseModel class.

        If arguments are provided in kwargs,
        it populates the instance attributes.
        If no arguments are provided, it adds the new instance to the storage.

        Args:
            *args: Non-keyword variable-length argument list.
            **kwargs: Variable-length keyword argument list.
        """
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.now()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.now()
        else:
            self.id = str(uuid4())
            self.created_at = self.updated_at = datetime.now()

    def save(self):
        """
        Updates the 'updated_at' attribute to the current date and time,
        then saves the changes to the storage.
        """
        self.updated_at = datetime.today()
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        '''deletes the current instance from the storage'''
        models.storage.delete(self)

    def to_dict(self):
        """
        Returns a dictionary representation of the instance.

        Returns:
            dict: Dictionary containing the instance attributes.
        """
        result_dict = self.__dict__.copy()
        result_dict["updated_at"] = self.updated_at.isoformat()
        result_dict["created_at"] = self.created_at.isoformat()
        result_dict["__class__"] = self.__class__.__name__
        return result_dict

    def __str__(self):
        """
        Returns a string representation of the instance.

        Returns:
            str: String representation containing
            class name, instance id, and attributes.
        """
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)
