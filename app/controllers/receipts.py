from flask import Blueprint, request, jsonify
from app.services import calculate_points, get_receipt, create_receipt
from app.schemas import ReceiptSchema

receipts_blueprint = Blueprint('receipts', __name__)

@receipts_blueprint.route('/process', methods=['POST'])
def process_receipt():
    data = request.json  
    schema = ReceiptSchema()
    try:
        receipt_data = schema.load(data)
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    receipt_id = create_receipt(receipt_data)
    
    return jsonify({"id": receipt_id}), 201

@receipts_blueprint.route('/<receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    receipt = get_receipt(receipt_id)
    if not receipt:
        return jsonify({"message": "Receipt not found"}), 404
    
    points = calculate_points(receipt)
    return jsonify({"points": points}), 200