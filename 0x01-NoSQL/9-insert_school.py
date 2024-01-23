#!/usr/bin/env python3
"""Script for MongoDB new document insertion."""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs
    Returns the new _id
    """
    new_doc = mongo_collection.insert_one(kwargs).inserted_id
    return new_doc
