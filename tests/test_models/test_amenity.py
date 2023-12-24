#!/usr/bin/python3
"""Defines unittests for models/amenity.py.
Unittest classes:
    TestAmenity_instantiation
    TestAmenity_save
    TestAmenity_to_dict
"""

import unittest
import os
import models
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Amenity class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_is_public_class_attribute(self):
        amenityo = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", amenityo.__dict__)

    def test_two_amenities_unique_ids(self):
        amenityo1 = Amenity()
        amenityo2 = Amenity()
        self.assertNotEqual(amenityo1.id, amenityo2.id)

    def test_two_amenities_different_created_at(self):
        amenityo1 = Amenity()
        sleep(0.05)
        amenityo2 = Amenity()
        self.assertLess(amenityo1.created_at, amenityo2.created_at)

    def test_two_amenities_different_updated_at(self):
        amenityo1 = Amenity()
        sleep(0.05)
        amenityo2 = Amenity()
        self.assertLess(amenityo1.updated_at, amenityo2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        amenityo = Amenity()
        amenityo.id = "123456"
        amenityo.created_at = amenityo.updated_at = dt
        amenityostr = amenityo.__str__()
        self.assertIn("[Amenity] (123456)", amenityostr)
        self.assertIn("'id': '123456'", amenityostr)
        self.assertIn("'created_at': " + dt_repr, amenityostr)
        self.assertIn("'updated_at': " + dt_repr, amenityostr)

    def test_instantiation_with_kwargs(self):
        """instantiation with kwargs test method"""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        amenityo = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(amenityo.id, "345")
        self.assertEqual(amenityo.created_at, dt)
        self.assertEqual(amenityo.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)

    def test_args_unused(self):
        amenityo = Amenity(None)
        self.assertNotIn(None, amenityo.__dict__.values())


class TestAmenity_save(unittest.TestCase):
    """Unittests for testing save method of the Amenity class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        amenityo = Amenity()
        sleep(0.05)
        first_updated_at = amenityo.updated_at
        amenityo.save()
        self.assertLess(first_updated_at, amenityo.updated_at)

    def test_two_saves(self):
        amenityo = Amenity()
        sleep(0.05)
        first_updated_at = amenityo.updated_at
        amenityo.save()
        second_updated_at = amenityo.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        amenityo.save()
        self.assertLess(second_updated_at, amenityo.updated_at)

    def test_save_with_arg(self):
        amenityo = Amenity()
        with self.assertRaises(TypeError):
            amenityo.save(None)

    def test_save_updates_file(self):
        amenityo = Amenity()
        amenityo.save()
        amid = "Amenity." + amenityo.id
        with open("file.json", "r") as f:
            self.assertIn(amid, f.read())


class TestAmenity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Amenity class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        amenityo = Amenity()
        self.assertIn("id", amenityo.to_dict())
        self.assertIn("created_at", amenityo.to_dict())
        self.assertIn("updated_at", amenityo.to_dict())
        self.assertIn("__class__", amenityo.to_dict())

    def test_to_dict_contains_added_attributes(self):
        amenityo = Amenity()
        amenityo.middle_name = "Holberton"
        amenityo.my_number = 98
        self.assertEqual("Holberton", amenityo.middle_name)
        self.assertIn("my_number", amenityo.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        amenityo = Amenity()
        amenityo_dict = amenityo.to_dict()
        self.assertEqual(str, type(amenityo_dict["id"]))
        self.assertEqual(str, type(amenityo_dict["created_at"]))
        self.assertEqual(str, type(amenityo_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        amenityo = Amenity()
        amenityo.id = "123456"
        amenityo.created_at = amenityo.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(amenityo.to_dict(), tdict)

    def test_to_dict_with_arg(self):
        amenityo = Amenity()
        with self.assertRaises(TypeError):
            amenityo.to_dict(None)

    def test_contrast_to_dict_dunder_dict(self):
        amenityo = Amenity()
        self.assertNotEqual(amenityo.to_dict(), amenityo.__dict__)


if __name__ == "__main__":
    unittest.main()
