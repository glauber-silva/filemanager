from flask import current_app

from flask_pymongo import PyMongo
from gridfs import GridFS


mongo = PyMongo()
fs = None


def init_db(app):
    # global fs
    mongo.init_app(app)
    # fs = GridFS(mongo.db)


# client = MongoClient(current_app.config.get("MONGO_URI"))
# db = client["filemanager"]
# fs = GridFS(db)
