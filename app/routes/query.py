from flask import Blueprint, request, jsonify
from bson import ObjectId, json_util
from pymongo.collection import Collection
from datetime import datetime

from app.models.subBillModel import SubBill, TAGS
from app.db import DATABASE

query_blueprint = Blueprint('query', __name__)


@query_blueprint.route('/date_query', methods=['GET'])
def date_query():
    try:
        print(request)
        # Get datetime objects from the query parameters
        start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')
        username = request.args.get('user')
        
        # Convert to JSON response object
        cursor = SubBill.fetchUserSubBillsByTime(DATABASE, username, start_date, end_date)
        json_data = json_util.dumps(list(cursor))

        return jsonify(json_data), 200
    except Exception as e:
        return f"An error occurred: {str(e)}", 400


@query_blueprint.route('/fetch_tags', methods=['GET'])
def fetch_tags():
    try:
        return jsonify(TAGS)
    except Exception as e:
        return f"An error occurred: {str(e)}", 400


@query_blueprint.route('/fetch_subbill', methods=['GET'])
def fetch_subbill():
    try:
        # Get datetime objects from the query parameters
        subbill_id = request.args.get('subbill_id')
        
        subbill_collection = Collection(DATABASE, "SubBill")
        res = subbill_collection.find_one({'_id': ObjectId(subbill_id)})

        return jsonify(res)
    except Exception as e:
        return f"An error occurred: {str(e)}", 400
