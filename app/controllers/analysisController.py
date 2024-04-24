from app.models.subBillModel import SubBill
from typing import List


def generateAnalayisData(sub_bill_list: List[SubBill]):
    total = 0
    for bill in sub_bill_list:
        total += bill.subBillDocument['total']

    return {
        "total": total
    }