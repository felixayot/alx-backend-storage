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
    top_ips = nginx_coll.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {"_id": 0, "ip": "$_id", "count": 1}}
        ])
    print("IPs:")
    for top_ip in top_ips:
        ip = top_ip.get("ip")
        count = top_ip.get("count")
    print(f"\t{ip}: {count}")
