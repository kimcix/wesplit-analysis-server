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
        print(request)
        # Get datetime objects from the query parameters
        start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')
        username = request.args.get('user')
        
        # Convert to JSON response object
        cursor = SubBill.fetchUserSubBillsByTime(DATABASE, username, start_date, end_date)
        json_data = dumps(list(cursor))

        return jsonify(json_data), 200
    except Exception as e:
        return f"An error occurred: {str(e)}", 400
    

@analysis_blueprint.route('/update_analytics', methods=['POST'])
def update_analytics():
    # Check if the request contains JSON data
    if request.is_json:
        # Get the JSON data from the request
        data = request.get_json()
        
        # Print the received JSON data
        print("Received JSON data:")
        print(data)

        # Querying the document with the given ID
        
        res = SubBill.updateSubBillTags(DATABASE, data['subBillId'], data['newTags'], data['newPayment'])
        # Optionally, you can return a response to the client
        if res:
            return jsonify({"message": "Data received successfully"}), 200
    # If the request does not contain JSON data, return an error response
    return jsonify({"error": "Invalid JSON data"}), 400

@analysis_blueprint.route('/user_analysis', methods=['GET'])
def user_analysis():
    try:
        print(request)
        # Get datetime objects from the query parameters
        username = request.args.get('username')
        
        # Convert to JSON response object
        cursor = SubBill.fetchSubBillsByUser(DATABASE, username)

        subbill_count = 0
        paid_count = 0
        total = 0.0
        total_owed = 0.0
        payback_time_avg = 0.0
        
        for subbill in cursor:
            subbill_count +=1
            total += subbill['total']
            if subbill['analytics']['paid']:
                paid_count += 1
                payback_time_avg += subbill['analytics']['payback_interval']
            else:
                total_owed += subbill['total']

        payback_time_avg /= subbill_count


        return_json = {
            "username": subbill["user_name"],
            "creator": subbill["creator"],
            "sub_bill_count": subbill_count,
            "total_accumulated": total,
            "total_owed": total_owed,
            "payback ratio": f"{paid_count}/{subbill_count}",
            "average_payback_time": f"{payback_time_avg if payback_time_avg > 0.0 else "N/A"}"
        }


        return jsonify(return_json), 200
    except Exception as e:
        return f"An error occurred: {str(e)}", 400
