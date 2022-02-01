from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="Item must have a price"
    )
    parser.add_argument(
        "store_id", type=int, required=True, help="Every item must have a store id"
    )

    @jwt_required()  # This can be put on every endpoint
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.to_json()

        return {"message": "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f"An item with name '{name}' already exists"}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error ocurred inserting the item"}, 500

        return item.to_json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item has been deleted"}, 200

        return {"message": "Item not found"}, 404

    def put(self, name):
        status_code = 200

        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)  # Inserts new if not present
            status_code = 201
        else:
            item.price = data["price"]  # Updates if price has changed
            item.store_id = data["store_id"]  # Or if both/store_id has changed

        item.save_to_db()

        return item.to_json(), status_code


class ItemList(Resource):
    def get(self):
        return {"items": [item.to_json() for item in ItemModel.query.all()]}, 200
