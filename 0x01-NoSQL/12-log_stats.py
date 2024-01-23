"""Script that provides some stats about Nginx logs stored in MongoDB."""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient("localhost", 27027)
    nginx_coll = client.logs.nginx
    print(f"{nginx_coll.count_documents({})} logs")
    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = nginx_coll.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")
    total_gets = nginx_coll.count_documents(
        {
            "method": "GET",
            "path": "/status"
        })
    print(f"{total_gets} status check")
