#!/usr/bin/python3
"""
module that creates users
"""

from models.base_model import BaseModel


class User(BaseModel):
    """
    a class User that inherits from BaseModel
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *args, **kwargs):
        """
        creates new user
        """
        super().__init__(self, *args, **kwargs)
