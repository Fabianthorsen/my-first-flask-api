from flask_restful import Resource

from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.to_json(), 200

        return {"message": "Store not found"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": f"Store with name {name} already exists"}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred while creating the store"}, 500

        return store.to_json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": "Store deleted"}, 200


class StoreList(Resource):
    def get(self):
        return {"stores": [store.to_json() for store in StoreModel.query.all()]}, 200