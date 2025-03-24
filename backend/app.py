import os
from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get MongoDB URI from environment variable
app.config["MONGO_URI"] = os.getenv("DATABASE_URI")
mongo = PyMongo(app)

@app.route('/')
def home():
    return "Flask with MongoDB is running!"

if __name__ == '__main__':
    app.run(debug=True)
