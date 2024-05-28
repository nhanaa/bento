from models.user import User
from utils.db import CosmosDB
import uuid

class UserService:
    def __init__(self):
        self.container = CosmosDB.get_container('Users')

    def create_user(self, email, name):
        user = self.get_user_by_email(email)
        if user:
            return user
        
        user = User(email, name)
        user.id = str(uuid.uuid4())
        self.container.create_item(body=user.to_dict())
        return user.to_dict()
    
    def get_user(self, query):
        items = list(self.container.query_items(query=query, enable_cross_partition_query=True))
        if not items:
            return None
        user = User.from_dict(items[0])
        return user.to_dict()
    
    def get_user_by_id(self, user_id):
        query = f"SELECT * FROM Users u WHERE u.id = '{user_id}'"
        return self.get_user(query)

    def get_user_by_email(self, email):
        query = f"SELECT * FROM Users u WHERE u.email = '{email}'"
        return self.get_user(query)
    
    def update_user(self, user, data):
        if not user:
            return None
        for key, value in data.items():
            setattr(user, key, value)

        self.container.replace_item(user.id, user.to_dict())
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
        self.container.delete_item(body=user.to_dict())
        return user.to_dict()

    def delete_user_by_id(self, user_id):
        user = self.get_user_by_id(user_id)
        return self.delete_user(user)

    def delete_user_by_email(self, email):
        user = self.get_user_by_email(email)
        return self.delete_user(user)
