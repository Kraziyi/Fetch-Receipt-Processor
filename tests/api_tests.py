# tests/test_receipt_processing.py

import unittest
from app import create_app

class TestReceiptProcessing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_process_receipt(self):
        receipt_data = {
            "retailer": "Target",
            "purchase_date": "2022-01-01",
            "purchase_time": "13:01",
            "items": [
                {"short_description": "Mountain Dew 12PK", "price": 6.49},
                {"short_description": "Emils Cheese Pizza", "price": 12.25},
                {"short_description": "Knorr Creamy Chicken", "price": 1.26},
                {"short_description": "Doritos Nacho Cheese", "price": 3.35},
                {"short_description": "Klarbrunn 12-PK", "price": 12.00}
            ],
            "total": 35.35
        }

        response = self.client.post('/receipts/process', json=receipt_data)
        self.assertEqual(response.status_code, 201)
        response_json = response.get_json()
        receipt_id = response_json.get("id")
        self.assertIsNotNone(receipt_id)

        response = self.client.get(f'/receipts/{receipt_id}/points')
        self.assertEqual(response.status_code, 200)
        points = response.get_json().get("points")
        self.assertEqual(points, 28) 

    def test_process_receipt_with_multiple_gatorade_items(self):
        receipt_data = {
            "retailer": "M&M Corner Market",
            "purchase_date": "2022-03-20",
            "purchase_time": "14:33",
            "items": [
                {"short_description": "Gatorade", "price": 2.25},
                {"short_description": "Gatorade", "price": 2.25},
                {"short_description": "Gatorade", "price": 2.25},
                {"short_description": "Gatorade", "price": 2.25}
            ],
            "total": 9.00
        }

        response = self.client.post('/receipts/process', json=receipt_data)
        self.assertEqual(response.status_code, 201)
        response_json = response.get_json()
        receipt_id = response_json.get("id")
        self.assertIsNotNone(receipt_id)

        response = self.client.get(f'/receipts/{receipt_id}/points')
        self.assertEqual(response.status_code, 200)
        points = response.get_json().get("points")
        self.assertEqual(points, 109)  

    def test_process_receipt_missing_fields(self):
        receipt_data = {
            "retailer": "Target",
            # "purchase_date" is missing

            "items": [
                {"short_description": "Mountain Dew 12PK", "price": 6.49},
            ],
            "total": 6.49
        }
        response = self.client.post('/receipts/process', json=receipt_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.get_json())  

    def test_process_receipt_invalid_date_format(self):
        receipt_data = {
            "retailer": "Target",
            "purchase_date": "01-01-2022",  # Invalid date format (should be YYYY-MM-DD)
            "purchase_time": "13:01",
            "items": [
                {"short_description": "Mountain Dew 12PK", "price": 6.49},
            ],
            "total": 6.49
        }
        response = self.client.post('/receipts/process', json=receipt_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.get_json())

    def test_process_receipt_invalid_price_type(self):
        receipt_data = {
            "retailer": "Target",
            "purchase_date": "2022-01-01",
            "purchase_time": "13:01",
            "items": [
                {"short_description": "Mountain Dew 12PK", "price": "six dollars"},  # Type should be float
            ],
            "total": 6.49
        }
        response = self.client.post('/receipts/process', json=receipt_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.get_json())

    def test_process_receipt_invalid_total_sum(self):   
        receipt_data = {
            "retailer": "Target",
            "purchase_date": "2022-01-01",
            "purchase_time": "13:01",
            "items": [
                {"short_description": "Mountain Dew 12PK", "price": 6.49},
                {"short_description": "Emils Cheese Pizza", "price": 12.25}
            ],
            "total": 100.00  # Total does not match sum of item prices
        }
        response = self.client.post('/receipts/process', json=receipt_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.get_json())

    def test_get_points_nonexistent_receipt_id(self):
        non_existent_receipt_id = "12345-nonexistent-id"
        response = self.client.get(f'/receipts/{non_existent_receipt_id}/points')
        self.assertEqual(response.status_code, 404)
        self.assertIn("message", response.get_json())

if __name__ == '__main__':
    unittest.main()
