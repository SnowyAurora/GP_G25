from app.user import User

class MedStaffUser(User):
    """
    Represents a medical staff user instance.
    """    

    def __init__(self, username, password, name, specialisation, email, phone_number):
        """
        Initializes a MedStaffUser instance.

        Args:
            username (str): The username for login authentication.
            password (str): The password associated with the account.
            name (str): Full name of the medical staff user.
            specialisation (str): Area of medical expertise.
            email (str): Professional email address.
            phone_number (str): Contact number of the medical staff user.

        This constructor calls the superclass (`User`) initializer to set up
        authentication attributes and adds fields relevant to medical staff.
        """
        super().__init__(username, password)
        self.name = name
        self.failed_attempts = 0
        self.lock_time = None
        self.specialisation = specialisation
        self.email = email
        self.phone_number = phone_number
