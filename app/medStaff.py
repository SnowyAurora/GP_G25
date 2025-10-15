from app.user import User

class MedStaffUser(User):
    def __init__(self, username, password,name,specialisation, email, phone_number):
        super().__init__(username, password)
        self.name = name
        self.specialisation = specialisation
        self.email = email
        self.phone_number = phone_number

