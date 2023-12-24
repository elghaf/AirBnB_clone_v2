#!/usr/bin/python3
"""The instanstiation of an object in the class FileStorage"""
import os

from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage

storage = DBStorage() if os.getenv(
    'HBNB_TYPE_STORAGE') == 'db' else FileStorage()
"""A DB instance representation of the models.
"""
storage.reload()
