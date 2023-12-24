#!/usr/bin/python3
""" The class to test file storage"""
import os
import unittest

from models import storage
from models.base_model import BaseModel


@unittest.skipIf(
    os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
class TestFileStorage(unittest.TestCase):
    """ The Class to check the file storage new model """
    def setUp(self):
        """ The funct to start the test """
        del_list = []
        for key in storage.all().keys():
            del_list.append(key)
        for key in del_list:
            del storage.all()[key]

    def tearDown(self):
        """ the function to Delete the given storage file  """
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_obj_list_empty(self):
        """ The function to check if the objects are empty or not"""
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ The function to chech if the new object succeeded """
        new = BaseModel()
        new.save()
        for obj in storage.all().values():
            temp = obj
        self.assertTrue(temp is obj)

    def test_all(self):
        """ The function to test if the __objects is properly returned """
        new = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """ The function to check if the File exists on BaseModel or not """
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """ The function to test if the Data is saved to file or not """
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """The function to check if the FileStorage succeeded """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """ The function to teste if the file is saved to __objects """
        new = BaseModel()
        new.save()
        storage.reload()
        loaded = None
        for obj in storage.all().values():
            loaded = obj
        self.assertEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    def test_reload_empty(self):
        """ The function to check getting informations from an empty file """
        with open('file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """ The function to check if sth happens if the file is not there """
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """ The function to test the BaseModel storage method """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """ The function to check the __file_path type string"""
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ The function to check the __objects file type  dict """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """The function to check if the  Key is correctely formatted """
        new = BaseModel()
        _id = new.to_dict()['id']
        temp = ''
        new.save()
        for key, value in storage.all().items():
            if value is new:
                temp = key
        self.assertEqual(temp, 'BaseModel' + '.' + _id)

    def test_storage_var_created(self):
        """ The function to check if the FileStorage object is there """
        from models.engine.file_storage import FileStorage
        self.assertEqual(type(storage), FileStorage)
