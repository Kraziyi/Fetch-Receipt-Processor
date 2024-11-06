from datetime import datetime
from math import ceil
import uuid
from app.models import Receipt, Item

receipt_db = {}

def calculate_points(receipt: Receipt) -> int:
    points = 0

    retailer_name = receipt.retailer
    points += sum(1 for char in retailer_name if char.isalnum())

    total = receipt.total
    if total.is_integer():
        points += 50
    if total % 0.25 == 0:
        points += 25

    items = receipt.items
    points += (len(items) // 2) * 5

    for item in items:
        description = item.shortDescription.strip()
        if len(description) % 3 == 0:
            price = item.price
            points += ceil(price * 0.2)

    purchase_date = receipt.purchaseDate
    try:
        day = datetime.strptime(purchase_date, '%Y-%m-%d').day
        if day % 2 != 0:
            points += 6
    except ValueError:
        pass

    purchase_time = receipt.purchaseTime
    try:
        time_obj = datetime.strptime(purchase_time, '%H:%M')
        if (time_obj.hour == 14 and time_obj.minute > 0) or (time_obj.hour == 15):
            points += 10
    except ValueError:
        pass

    return points


def create_receipt(receipt_data):
    items = [Item(item['short_description'], item['price']) for item in receipt_data['items']]
    receipt = Receipt(
        retailer=receipt_data['retailer'],
        purchase_date=receipt_data['purchase_date'],
        purchase_time=receipt_data['purchase_time'],
        items=items,
        total=receipt_data['total']
    )
    receipt_id = str(uuid.uuid4())
    store_receipt(receipt_id, receipt)
    return receipt_id

def create_receipt(receipt_data):
    items = [Item(item['short_description'], item['price']) for item in receipt_data['items']]
    receipt = Receipt(
        retailer=receipt_data['retailer'],
        purchase_date=receipt_data['purchase_date'],
        purchase_time=receipt_data['purchase_time'],
        items=items,
        total=receipt_data['total']
    )
    receipt_id = str(uuid.uuid4())
    store_receipt(receipt_id, receipt)
    return receipt_id

def store_receipt(receipt_id: str, receipt: Receipt):
    receipt_db[receipt_id] = receipt

def get_receipt(receipt_id: str) -> Receipt:
    return receipt_db.get(receipt_id)