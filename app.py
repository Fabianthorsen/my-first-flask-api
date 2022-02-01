from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.register import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"  # The location of the db
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "fabian"

api = Api(
    app
)  # Allow us to easily add resources to the app (GET, POST, PUT, DELETE and so on)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth endpoint

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

api.add_resource(
    UserRegister, "/register"
)  # When this is accessed, the UserRegister method will be called

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
