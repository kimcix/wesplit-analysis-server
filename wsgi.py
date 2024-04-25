from flask import Flask
from flask_cors import CORS
from app.routes.analysis import analysis_blueprint
from app.routes.query import query_blueprint

from app.controllers.subBillInputController import consume

def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    CORS(app)
    
    app.register_blueprint(analysis_blueprint)
    app.register_blueprint(query_blueprint)

    # Initialize RabbitMQ consumer 
    consume()

    # Return the Flask app
    return app

if __name__ == "__main__":
    # Create the Flask app
    app = create_app()
