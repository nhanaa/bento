import datetime
import uuid

class User:
    def __init__(self, email, name):
        self.id = str(uuid.uuid4())
        self.email = email
        self.name = name
        self.is_deactivated = False
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    def to_dict(self):
        return {
            'id': str(self.id),
            'email': self.email,
            'name': self.name,
            'is_deactivated': self.is_deactivated,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
        }

    # Create User object from dict
    @classmethod
    def from_dict(cls, data):
        user = cls(data['email'], data['name'])
        if 'id' in data: user.id = data['id']
        if 'created_at' in data: user.created_at = data['created_at']
        if 'updated_at' in data: user.updated_at = data['updated_at']
        
        return user
