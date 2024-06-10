from ..models.user import User
from ..app import db
from ..utils.utils import jsonify_document
from bson import ObjectId


class UserService:
    def __init__(self):
        if "users" not in db.list_collection_names():
            db.create_collection("users")
        self.collection = db.get_collection("users")

    def create_user(self, email, name):
        user = self.get_user_by_email(email)
        if user:
            return user

        user = User(email, name)
        result = self.collection.insert_one(user.to_dict())
        inserted_id = result.inserted_id
        user = self.collection.find_one({"_id": ObjectId(inserted_id)})

        return jsonify_document(user)

    def get_user_by_id(self, user_id):
        user = self.collection.find_one({"_id": ObjectId(user_id)})
        return jsonify_document(user)

    def get_user_by_email(self, email):
        user = self.collection.find_one({"email": email})
        return jsonify_document(user)

    def update_user_by_id(self, user_id, data):
        result = self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": data})
        if result.modified_count > 0:
            updated_user = self.collection.find_one({"_id": ObjectId(user_id)})
            return jsonify_document(updated_user)
        else:
            return None

    def update_user_by_email(self, email, data):
        result = self.collection.update_one({"email": email}, {"$set": data})
        if result.modified_count > 0:
            updated_user = self.collection.find_one({"email": email})
            return jsonify_document(updated_user)
        else:
            return None

    def delete_user_by_id(self, user_id):
        user = self.collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return None
        self.collection.delete_one({"_id": ObjectId(user_id)})
        return jsonify_document(user)

    def delete_user_by_email(self, email):
        user = self.collection.delete_one({"email": email})
        if not user:
            return None
        self.collection.delete_one({"email": email})
        return jsonify_document(user)
