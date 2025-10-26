from app.user import User

class PatientUser(User):
    def __init__(self, username, password,name, email, phone_number):
        super().__init__(username, password)
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.failed_attempts = 0
        self.lock_time = None
        self.assigned_caretaker = []
        self.personal_preferences = []
        self.clinical_observations = []

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "assigned_caretaker": self.assigned_caretaker,
            "personal_preferences": self.personal_preferences,
            "clinical_observations": self.clinical_observations,
            "failed_attempts": getattr(self, "failed_attempts", 0),
            "lock_time": getattr(self, "lock_time", None)
        }
