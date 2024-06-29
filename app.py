import os
from flask import Flask
from routes import pages
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    # 連上 Cluster0
    client = MongoClient(os.getenv("MONGODB_URI"))
    # 連上數據庫
    app.db = client.get_default_database()
    # blue print
    app.register_blueprint(pages)

    return app