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

# Initialize API with proper configuration
api.init_app(app, prefix='/api')

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

# Initialize metrics collection on first request
@app.before_request
def initialize_metrics_collection():
    """Initialize metrics collection on first request."""
    if not hasattr(app, '_metrics_initialized'):
        collection_manager.start()
        app._metrics_initialized = True

if __name__ == '__main__':
    import sys
    port = int(os.getenv('PORT', 5000))
    # Allow specifying port via command-line argument
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port argument: {sys.argv[1]}. Using default port {port}.")
    app.run(host='0.0.0.0', port=port) 