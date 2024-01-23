#!/usr/bin/env python3
"""Script for MongoDB specific collection document query."""


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of school with a specific topic.
    topic (string) topic being searched
    """
    return mongo_collection.find({"topics": topic})
