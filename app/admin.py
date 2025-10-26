from app.user import User

class AdminUser(User):
    """
    Represents an administrative user instance
    """

    def __init__(self, username, password):
        """
        Initializes an AdminUser instance.

        Args:
            username (str): The username of the admin user.
            password (str): The password associated with the admin user.

        The constructor calls the superclass (`User`) initializer to set up
        base user attributes and initializes additional fields for
        failed login attempt tracking and account locking.
        """
        super().__init__(username, password)
        self.failed_attempts = 0
        self.lock_time = None
