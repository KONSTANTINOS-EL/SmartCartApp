from datetime import datetime

class User:
    def __init__(self, username, email, password, role = "user"):
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return{
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "created_at": self.created_at
        }