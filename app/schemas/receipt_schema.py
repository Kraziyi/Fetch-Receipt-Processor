from marshmallow import Schema, fields, validates, ValidationError, validates_schema
from datetime import datetime

class ItemSchema(Schema):
    short_description = fields.Str(required=True)
    price = fields.Float(required=True)

class ReceiptSchema(Schema):
    retailer = fields.Str(required=True)
    purchase_date = fields.Str(required=True)
    purchase_time = fields.Str(required=True)
    items = fields.List(fields.Nested(ItemSchema), required=True)
    total = fields.Float(required=True)

    @validates("purchase_date")
    def validate_purchase_date(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValidationError("purchase_date must be in YYYY-MM-DD format.")
        
    @validates("purchase_time")
    def validate_purchase_time(self, value):
        try:
            datetime.strptime(value, "%H:%M")
        except ValueError:
            raise ValidationError("purchase_time must be in HH:MM format.")

    @validates_schema
    def validate_total_sum(self, data, **kwargs):
        items_total = sum(item['price'] for item in data.get('items', []))
        if not round(items_total, 2) == round(data.get('total', 0), 2):
            raise ValidationError("Total does not match sum of item prices.", field_name="total")
