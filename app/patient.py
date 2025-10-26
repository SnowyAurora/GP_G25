from app.user import User

class PatientUser(User):
    """
    Represents a patient user instance.
    """

    def __init__(self, username, password, name, email, phone_number):
        """
        Initializes a PatientUser instance.

        Args:
            username (str): Username used for login authentication.
            password (str): Password associated with the account.
            name (str): Full name of the patient.
            email (str): Email address of the patient.
            phone_number (str): Contact number of the patient.

        The constructor calls the superclass (`User`) initializer for
        authentication attributes, then initializes patient-specific details
        """
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
        """
        Returns a dictionary representation of the PatientUser instance.

        This method is typically used for data serialization or
        database/storage operations.

        Returns:
            dict: A dictionary containing the patient's user details,
            account status, and related records.
        """
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
