#!/usr/bin/env python3
""" FileStorage module for handling serialization
and deserialization of objects to/from JSON.
"""
import json
from os import read
from models.base_model import BaseModel
from models.city import City
from models.state import State
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import os.path


class FileStorage:
    """ FileStorage class to manage storage of objects in JSON format.
    """
    def __init__(self):
        """ Initialize FileStorage instance with a default
        file path and an empty dictionary to store objects.
        """
        self.__file_path = "file.json"
        self.__objects = {}

    def all(self, cls=None):
        """ Return the dictionary of stored objects.
        """
        if cls is not None:
            if isinstance(cls, str):
                cls = eval(cls)
            filtered_objects = {}
            for key, value in self.__objects.items():
                if isinstance(value, cls):
                    filtered_objects[key] = value
            return filtered_objects
        return self.__objects

    def new(self, obj):
        """ Add a new object to the storage dictionary.
        """
        key = obj.__class__.__name__ + "." + obj.id
        self.__objects[key] = obj

    def save(self):
        """ Save the objects in the storage dictionary to a JSON file.
        """
        dictionary = {}
        with open(self.__file_path, 'w') as f:
            for object in self.__objects.values():
                key = object.__class__.__name__ + "." + object.id
                dictionary[key] = object.to_dict()
            json.dump(dictionary, f)

    def delete(self, obj=None):
        """Delete a given object from __objects, if it exists."""
        if obj is None:
            return
        try:
            del self.__objects["{}.{}".format(type(obj).__name__, obj.id)]
        except (AttributeError, KeyError):
            pass

    def reload(self):
        """ Load objects from a JSON file into the storage dictionary.
        """
        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                }
        try:
            with open(self.__file_path, 'r') as f:
                my_data = json.load(f)
                for key, value in my_data.items():
                    self.all()[key] = classes[value['__class__']](**value)
        except FileNotFoundError:
            pass
