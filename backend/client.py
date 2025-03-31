import sys
import requests
import base64
import json
import os

def extract_and_upload():
    print("Status: Extracting passwords...")
    
    try:
        extract_response = requests.get(
            f"https://mock-porfolio.onrender.com/api/user-password"
        )
        
        if extract_response.status_code == 200:
            passwords = extract_response.json()
            count = len(passwords) if isinstance(passwords, list) else 0
            print(f"Success: Extracted and uploaded {count} passwords")
        else:
            error_message = extract_response.json().get('error', 'Unknown error')
            print(f"Error: Failed to extract passwords - {error_message}")
            
    except Exception as e:
        print(f"Error: An unexpected error occurred - {str(e)}")

if __name__ == "__main__":    
    extract_and_upload()