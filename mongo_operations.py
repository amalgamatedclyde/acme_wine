__author__ = 'clyde'

from pymongo import MongoClient

client = MongoClient('mongodb://admin:ZaT5Whr2p1@ds017514.mlab.com:17514/acme')
db = client.acme

def save2mongo(validated_records):
    orders = db.orders
    result = orders.insert_many(validated_records)
    return result.acknowledged


def retrieve_valid_orders():
    orders = db.orders
    valid_orders = [order for order in orders.find({"valid": True})]
    for d in valid_orders:
        d.pop("_id", None)
    return valid_orders
