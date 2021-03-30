# pylint: disable=locally-disabled, multiple-statements, fixme, line-too-long, import-error
""" user model """
class User:
    """ constructor for the user """
    def __init__(self, name, password, email, roles):
        self._name = name
        self._password = password
        self._email = email
        self._roles = roles


    # using property decorator
    # a getter function for the name
    @property
    def name(self):
        """ getter for user name """
        return self._name

    # a setter function for name
    @name.setter
    def set_name(self, user_name):
        """ setter for user name """
        self._name = user_name

    # using property decorator
    # a getter function for the password
    @property
    def password(self):
        """ getter for user password """
        return self._password

    # a setter function for name
    @password.setter
    def set_password(self, user_password):
        self._password = user_password

    # using property decorator
    # a getter function for the email
    @property
    def email(self):
        """ getter for user email """
        return self._email

    # a setter function for name
    @email.setter
    def set_email(self, user_email):
        """ setter for user email """
        self._email = user_email

    # using property decorator
    # a getter function for the email
    @property
    def roles(self):
        """ getter for user roles """
        return self._roles

    # a setter function for name
    @roles.setter
    def set_roles(self, user_roles):
        """ setter for user roles """
        self._roles = user_roles
