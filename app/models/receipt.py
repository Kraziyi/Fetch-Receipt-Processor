class Receipt:
    def __init__(self, retailer, purchase_date, purchase_time, items, total):
        self.retailer = retailer
        self.purchaseDate = purchase_date
        self.purchaseTime = purchase_time
        self.items = items
        self.total = total

class Item:
    def __init__(self, short_description, price):
        self.shortDescription = short_description
        self.price = price
