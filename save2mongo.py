__author__ = 'clyde'

from pymongo import MongoClient, i

client = MongoClient('mongodb://admin:ZaT5Whr2p1@ds017514.mlab.com:17514/acme')
db = client.orders

def save2mongo(validated_records):
    db.insert_many(validated_records)