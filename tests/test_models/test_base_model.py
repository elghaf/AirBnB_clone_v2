#!/usr/bin/python3
""" unittest for models/base_model.py
"""
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class Test_BaseModel(unittest.TestCase):
    """ test instantiation of BaseModel """
    def test_BaseModel_init(self):
        """ test instantiation of BaseModel """
        base_model = BaseModel()
        self.assertEqual(BaseModel, type(BaseModel()))
        self.assertTrue(hasattr(base_model, "id"))

    def test_BaseModel_created_at_instance_from_datetime(self):
        """ test created_at """
        base_model = BaseModel()
        self.assertTrue(isinstance(base_model.created_at, datetime))

    def test_BaseModel_updated_at_instance_from_datetime(self):
        """ test updated_at """
        base_model = BaseModel()
        self.assertTrue(isinstance(base_model.updated_at, datetime))

    def test_BaseModel_created_not_equal(self):
        """ create two objects at different time """
        base_model = BaseModel()
        sleep(0.1)
        base_model_new = BaseModel()
        self.assertNotEqual(base_model.created_at, base_model_new.created_at)

    def test_BaseModel_save(self):
        """ Test save method """
        base_model = BaseModel()
        base_model.save()
        self.assertNotEqual(base_model.created_at, base_model.updated_at)

    def test_BaseModel_dict_keys(self):
        """ test to_dict method correct keys """
        base_model = BaseModel()
        my_data = base_model.to_dict()

        self.assertIn("id", my_data)
        self.assertIn("created_at", my_data)
        self.assertIn("updated_at", my_data)
        self.assertIn("__class__", my_data)

    def test_BaseModel_str(self):
        """ test str method. assertEqual: a and b are equal"""
        base_model = BaseModel()
        self.assertEqual(type(str(base_model)), str)

    def test_BaseModel_list_type(self):
        """ test to_dict if contains added attributes """
        base_model = BaseModel()
        my_data = base_model.to_dict()
        self.assertEqual(type(my_data), dict)


if __name__ == "__main__":
    unittest.main()
