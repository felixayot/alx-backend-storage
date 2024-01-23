#!/usr/bin/env python3
"""Script for student score average function."""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score
    The top must be ordered
    The average score must be part of each item returns with key = averageScore
    """
    student_score = mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}}
        }, {"$sort": {"averageScore": -1}}])
    return student_score
