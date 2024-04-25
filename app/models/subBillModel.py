from datetime import datetime

from pymongo.collection import Collection
from pymongo.database import Database
from bson import ObjectId

"""
subBillDocument = {
            "masterbill":master_bill_id,
            "masterbill_name": master_bill_name,
            "user_name":user_name,
            "creator": user_name,
            "creation_time":creation_time,
            "item_list":item_list,
            "total":total,
            "analytics": {
                "paid":False,
                "payment_time":None,
                "payback_interval":None,
                "tags":[]
            }
"""

TAGS = ["food", "groceries", "rent", "bills", "entertainment"]

class SubBill():
    @staticmethod
    def fetchSubBillsByUser(db: Database, user):
        sub_bill_collection = Collection(db, "SubBill")
        return sub_bill_collection.find({
            "user_name": user,
        })
    
    @staticmethod
    def fetchUserSubBillsByTime(db: Database, user, start_datetime, end_datetime):
        sub_bill_collection = Collection(db, "SubBill")
        return sub_bill_collection.find({
            "user_name": user,
            "creation_time": {
                "$gte": start_datetime,
                "$lt": end_datetime
            },
        })

    @staticmethod
    def updateSubBillTags(db: Database, id , tag_list, payment):
        # Querying the document with the given ID
        sub_bill_collection = Collection(db, "SubBill")
        document = sub_bill_collection.find_one({'_id': ObjectId(id)})
        print(document)
        print(payment)
        if document:
            # Update the desired field
            sub_bill_collection.update_one({'_id': ObjectId(id)}, 
                                           {'$set': {"analytics.tags": tag_list,
                                                     "analytics.paid": payment["paid"],
                                                     "analytics.payment_time": payment["payment_time"],
                                                     "analytics.payback_interval": payment["payback_interval"]}
                                           })
            return True
        return False

    def __init__(self, master_bill_id, masterbill_name, user_name, creator, creation_time, item_list, total: float):
        self.subBillDocument = {
            "masterbill":ObjectId(master_bill_id),
            "masterbill_name": masterbill_name,
            "user_name":user_name,
            "creator": creator,
            "creation_time":datetime.strptime(creation_time, '%Y-%m-%dT%H:%M:%SZ'),
            "item_list":item_list,
            "total":total,
            "analytics": {
                "paid":False,
                "payment_time":None,
                "payback_interval":None,
                "tags":[]
            }
        }
    
    def setAnalytics(self, paid=False, payment_time="", payback_interval=0.0, tags=[]):
        self.subBillDocument['analytics']['paid'] = paid
        self.subBillDocument['analytics']['payment_time'] = payback_interval
        self.subBillDocument['analytics']['payback_interval'] = payback_interval
        self.subBillDocument['analytics']['tags'] = tags

    def insertSubBill(self,  db: Database):
        sub_bill_collection = Collection(db, "SubBill")
        print(sub_bill_collection.insert_one(self.subBillDocument))