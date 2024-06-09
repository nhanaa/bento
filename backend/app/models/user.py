import datetime

class User:
    def __init__(self, email, name):
        self.email = email
        self.name = name
        self.is_deactivated = False
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    def to_dict(self):
        return {
            'email': self.email,
            'name': self.name,
            'is_deactivated': self.is_deactivated,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    # Create User object from dict
    @classmethod
    def from_dict(cls, data):
        user = cls(data['email'], data['name'])
        return user
