#!/usr/bin/env python3
"""Script for MongoDB new document update."""


def update_topics(mongo_collection, name, topics):
    """
    Changes all topics of a school document based on the name
    name (string) will be the school name to update
    topics (list of strings) will be the list of topics
    approached in the school
    """
    document = {"name": name}
    updated_values = {"$set": {"topics": topics}}
    updated_doc = mongo_collection.update_many(document, updated_values)
    return updated_doc
