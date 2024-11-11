from flask import current_app

from flask_pymongo import PyMongo
from gridfs import GridFS


mongo = PyMongo()

# client = MongoClient(current_app.config.get("MONGO_URI"))
# db = client["filemanager"]
# fs = GridFS(db)
