__author__ = 'clyde'

from pymongo import MongoClient


mongolab_uri = 'mongodb://admin:rjTzHb1AHv@ds013165-a0.mlab.com:13165,ds013165-a1.mlab.com:13165/acme?replicaSet=rs-ds013165'
client = MongoClient(mongolab_uri,
                     connectTimeoutMS=30000,
                     socketTimeoutMS=None,
                     socketKeepAlive=True,
                     j=False)
db = client.acme


def save2mongo(validated_records):
    orders = db.orders
    r = orders.insert_many(validated_records)
    return r.acknowledged

def retrieve_valid_orders():
    orders = db.orders
    valid_orders = [order for order in orders.find({"valid": True}, projection={'id': 1, 'name': 1, 'valid': 1, '_id': 0})]
    return valid_orders


def retrieve_all_orders():
    orders = db.orders
    orders = [order for order in orders.find(projection={'id': 1, 'name': 1, 'valid': 1, '_id': 0})]
    return orders

def retrieve_one(order_num):
    orders = db.orders
    order = orders.find_one({'id': order_num}, projection={'_id': 0, "name": 1, "state": 1, "zipcode": 1,
                                                           "birthday": 1, "valid": 1, "errors": 1})
    return order
