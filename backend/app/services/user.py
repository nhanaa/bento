from flask import app
from pymongo import MongoClient
from utils.db import MongoDB
from models.user import User
import uuid

class UserService:
    def __init__(self):
        self.collection = MongoDB.get_collection('Users')

    def create_user(self, email, name):
        user = self.get_user_by_email(email)
        if user:
            return {"message": "User already exists"}, True
        
        user = User(email, name)
        user.id = str(uuid.uuid4())
        self.collection.insert_one(user.to_dict())
        return user.to_dict(), False
    
    def get_user(self, query):
        item = self.collection.find_one(query)
        if not item:
            return None
        user = User.from_dict(item)
        return user.to_dict()
    
    def get_user_by_id(self, user_id):
        query = {"id": user_id}
        return self.get_user(query)

    def get_user_by_email(self, email):
        query = {"email": email}
        return self.get_user(query)
    
    def update_user(self, user, data):
        if not user:
            return None
        for key, value in data.items():
            setattr(user, key, value)

        self.collection.update_one({"id": user.id}, {"$set": user.to_dict()})
        return user

    def update_user_by_id(self, user_id, data):
        user = self.get_user_by_id(user_id)
        return self.update_user(user, data)

    def update_user_by_email(self, email, data):
        user = self.get_user_by_email(email)
        return self.update_user(user, data)
    
    def delete_user(self, user):
        if not user:
            return None
        self.collection.delete_one({"id": user.id})
        return user.to_dict()

    def delete_user_by_id(self, user_id):
        user = self.get_user_by_id(user_id)
        return self.delete_user(user)

    def delete_user_by_email(self, email):
        user = self.get_user_by_email(email)
        return self.delete_user(user)
