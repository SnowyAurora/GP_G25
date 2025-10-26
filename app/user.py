class User:
    """A base class for all users in the system."""
    def __init__(self, user_id, password):
        self.username = user_id
        self.password = password

