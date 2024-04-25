from flask import Flask
from flask_cors import CORS
from app.routes.analysis import analysis_blueprint
from app.routes.query import query_blueprint
from threading import Thread

from app.controllers.subBillInputController import consume

def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    CORS(app)
    
    app.register_blueprint(analysis_blueprint)
    app.register_blueprint(query_blueprint)

    # Initialize RabbitMQ consumer 
    # consume()

    # Return the Flask app
    print("Successfully started Flask")
    return app

# Start app
if __name__ == '__main__':
    consumer_thread = Thread(target=consume)
    consumer_thread.daemon = True
    consumer_thread.start()

    app= create_app()

    app.run(host='localhost', port=5003)
