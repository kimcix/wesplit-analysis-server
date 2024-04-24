from flask import Blueprint, request, jsonify
from bson.json_util import dumps
from pymongo.collection import Collection

from app.models.subBillModel import SubBill, TAGS
from app.db import DATABASE

query_blueprint = Blueprint('query', __name__)


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
        res = subbill_collection.find_one({'_id': subbill_id})

        return jsonify(res)
    except Exception as e:
        return f"An error occurred: {str(e)}", 400
