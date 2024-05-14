class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def from_dict(user_dict):
        return User(user_dict['username'], user_dict['email'], user_dict['password'])

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password
        }