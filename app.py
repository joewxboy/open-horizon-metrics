from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from src.api import api
from src.utils.database import Base, engine
from src.collectors.collection_manager import CollectionManager

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
CORS(app)

# Initialize API
api.init_app(app)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize metrics collection
service_names = os.getenv('SERVICE_NAMES', '').split(',')
collection_interval = int(os.getenv('COLLECTION_INTERVAL', '60'))
collection_manager = CollectionManager(service_names, collection_interval)

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200

@app.before_first_request
def start_metrics_collection():
    """Start metrics collection when the first request is received."""
    collection_manager.start()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 