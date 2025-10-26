from app.user import User

class AdminUser(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.failed_attempts = 0
        self.lock_time = None



