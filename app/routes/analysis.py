from flask import Blueprint, request, jsonify
from bson.json_util import dumps
from datetime import datetime

from app.models.subBillModel import SubBill
from app.db import DATABASE

analysis_blueprint = Blueprint('analysis', __name__)

"""
    Return a query
"""
@analysis_blueprint.route('/date_query', methods=['GET'])
def date_query():
    try:
        # Get datetime objects from the query parameters
        start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')
        
        # Convert to JSON response object
        cursor = SubBill.fetchSubBillsByTime(DATABASE, start_date, end_date)
        json_data = dumps(list(cursor))

        return jsonify(json_data), 200
    except Exception as e:
        return f"An error occurred: {str(e)}", 400
    

@analysis_blueprint.route('/update_tags', methods=['POST'])
def update_tags():
    # Check if the request contains JSON data
    if request.is_json:
        # Get the JSON data from the request
        data = request.get_json()
        
        # Print the received JSON data
        print("Received JSON data:")
        print(data)

        # Querying the document with the given ID
        
        res = SubBill.updateSubBillTags(DATABASE, data['subBillId'], data['newTags'])
        
        # Optionally, you can return a response to the client
        if res:
            return jsonify({"message": "Data received successfully"}), 200
    # If the request does not contain JSON data, return an error response
    return jsonify({"error": "Invalid JSON data"}), 400
