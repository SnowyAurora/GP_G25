from user import User

class MedStaffUser(User):
    def __init__(self, username, password,name):
        super().__init__(username, password)
        self.name = name

