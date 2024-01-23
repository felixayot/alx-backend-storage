#!/usr/bin/env python3
"""Script for MongoDB collection documents list function."""


def list_all(mongo_collection):
    """
    Lists all documents in a collection.
    Returns an empty list if no document in the collection.
    """
    if mongo_collection.count_documents({}) == 0:
        return []
    documents = mongo_collection.find()
    return documents
