#!/usr/bin/python3
"""
module that creates review
"""

from models.base_model import BaseModel


class Review(BaseModel):
    """
    class review that inherits from BaseModel
    """

    place_id = ""
    user_id = ""
    text = ""

    def __init__(self, *args, **kwargs):
        """
        creates new review
        """
        super().__init__(self, *args, **kwargs)
