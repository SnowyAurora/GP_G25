class User:
    """
    A base class representing a generic user in the system.
    """

    def __init__(self, username, password):
        """
        Initializes a User instance.

        Args:
            username (str): The username for the account.
            password (str): The password for the account.

        This constructor sets up the basic authentication attributes
        common to all user types. 
        """
        self.username = username
        self.password = password
