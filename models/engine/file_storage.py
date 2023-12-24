#!/usr/bin/python3
"""The presentation of module class for the class file storage management for hbnb clone"""
import json
import os
from importlib import import_module


class FileStorage:
    """The functionality of this class is to manage storage of hbnb in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def __init__(self):
        """The initialization a FileStorage occurence"""
        self.model_classes = {
            'BaseModel': import_module('models.base_model').BaseModel,
            'User': import_module('models.user').User,
            'State': import_module('models.state').State,
            'City': import_module('models.city').City,
            'Amenity': import_module('models.amenity').Amenity,
            'Place': import_module('models.place').Place,
            'Review': import_module('models.review').Review
        }

    def all(self, cls=None):
        """Displays a dictionary of stored models updated"""
        if cls is None:
            return self.__objects
        else:
            filtered_dict = {}
            for key, value in self.__objects.items():
                if type(value) is cls:
                    filtered_dict[key] = value
            return filtered_dict

    def delete(self, obj=None):
        """The funct deletes an object from the dictionary"""
        if obj is not None:
            obj_key = obj.to_dict()['__class__'] + '.' + obj.id
            if obj_key in self.__objects.keys():
                del self.__objects[obj_key]

    def new(self, obj):
        """ Displays new object added to the dictionary"""
        self.__objects.update(
            {obj.to_dict()['__class__'] + '.' + obj.id: obj}
        )

    def save(self):
        """The new  dictionary saved to a file"""
        with open(self.__file_path, 'w') as file:
            i = {}
            for key, val in self.__objects.items():
                i[key] = val.to_dict()
            json.dump(i, file)

    def reload(self):
        """Extracts information of the dictionary from file"""
        classes = self.model_classes
        if os.path.isfile(self.__file_path):
            i = {}
            with open(self.__file_path, 'r') as file:
                i = json.load(file)
                for key, val in i.items():
                    self.all()[key] = classes[val['__class__']](**val)

    def close(self):
        """The funct to close the storage engine definitely."""
        self.reload()
