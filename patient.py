from user import User

class PatientUser(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.assigned_caretaker = []
        self.personal_preferences = []
        self.clinical_observations = []

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "assigned_caretaker": self.assigned_caretaker,
            "personal_preferences": self.personal_preferences,
            "clinical_observations": self.clinical_observations
        }
