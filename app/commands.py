import click
from flask.cli import with_appcontext
from app.db import mongo

@click.command(name="about")
@with_appcontext
def about():
    return "Simple service to manage files"

@click.command(name="create_collection")
@click.argument("collection_name")
@with_appcontext
def create_collection(collection_name):
    if collection_name not in mongo.db.list_collection_names():
        mongo.db.create_collection(collection_name)
        print(f"Collection '{collection_name}' criada no banco '{mongo.db.name}'.")