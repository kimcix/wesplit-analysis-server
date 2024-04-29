from flask import Blueprint, Response, request, jsonify
from bson import ObjectId, json_util
from pymongo.collection import Collection
from datetime import datetime

from app.models.subBillModel import SubBill, TAGS
from app.controllers.subBillInputController import SUB_INBOX
from app.controllers.subscriptionInboxController import User
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
        
        end_date_with_time = datetime.combine(end_date, datetime.max.time())

        # Convert to JSON response object
        cursor = SubBill.fetchUserSubBillsByTime(DATABASE, username, start_date, end_date_with_time)
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


"""
Basic SSE endpoint
"""
@query_blueprint.route('/stream_start', methods=['GET'])
def stream_start():
    user = request.args.get('user')
    user_instance = User(user)
    SUB_INBOX.addSubscriber(user_instance)
    print(f"Start stream for {user}")
    # Subscribe user to stream
    def events():
        yield "data: ping\n\n"
        try:
            while True:
                if user_instance.notify_client():
                    print(f"Notifying {user_instance.username}")
                    yield f"data: reload\n\n"
                
                if user_instance.connection_lost:
                    raise Exception("Connection lost for {user}")
        except:
            print(f"End stream for {user}")
    
    return Response(events(), content_type='text/event-stream')

@query_blueprint.route('/stream_end', methods=['GET'])
def stream_end():
    user = request.args.get('user')
    user_instance = SUB_INBOX.findSubscriberByName(user)
    if user_instance is not None:
        SUB_INBOX.removeSubscriber(user_instance)
        user_instance.mark_connection_lost()

    return jsonify(None), 204

    