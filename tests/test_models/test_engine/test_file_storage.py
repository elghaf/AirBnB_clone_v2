#!/usr/bin/env python3
"""
Unitest for the FileStorage class
"""
import os
import unittest
import models
from models import storage
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class Test_FileStorage(unittest.TestCase):

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        """check if all method is working"""

        self.assertIsNotNone(storage.all())
        self.assertEqual(dict, type(storage.all()))
        self.assertIsNotNone(models.engine.file_storage.FileStorage().all)


    def test_new(self):
        base_model = BaseModel()
        storage.new(base_model)

        self.assertIsNotNone(models.engine.file_storage.FileStorage().new)
        self.assertIn("BaseModel." + base_model.id, storage.all().keys())
        self.assertIn(base_model, storage.all().values())

    def test_save(self):
        """check if save method is working"""

        base_model = BaseModel()
        storage.new(base_model)
        storage.save()
        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn("BaseModel." + base_model.id, save_text)
        self.assertIsNotNone(models.engine.file_storage.FileStorage().save)

    def test_reload(self):
        """check if reload method is working"""

        self.assertIsNotNone(models.engine.file_storage.FileStorage().reload)


if __name__ == '__main__':
    unittest.main()
