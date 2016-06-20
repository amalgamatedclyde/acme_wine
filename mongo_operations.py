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
