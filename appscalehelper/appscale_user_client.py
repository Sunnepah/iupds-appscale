#!/usr/bin/env python
""" Handlers interface to the user/apps soap server in AppScale. """

# General-purpose Python libraries
import time
import ssl
import re
import cgi

# Third-party imports
import SOAPpy

from key_name import KEY_NAME
from uaserver_host import UA_SERVER_IP
from local_state import LocalState


class AppscaleUserClient:
    """UserAppClient provides callers with an interface to AppScale's
    UserAppServer daemon.

    The UserAppServer is a SOAP-exposed service that is responsible for handling
    user and application-level data. It uses the database-agnostic AppDB interface
    to enable callers to read and write database information, without needing to
    be concerned with the particulars of the database that AppScale is running on.
    """

    # The port that the UserAppServer runs on by default.
    PORT = 4343

    # A str that contains all of the authorizations that an AppScale cloud
    # administrator should be granted.
    ADMIN_CAPABILITIES = ":".join(["upload_app"])

    # The initial amount of time we should sleep when waiting for UserAppServer
    # metadata to change state.
    STARTING_SLEEP_TIME = 1

    # The maximum amount of time we should sleep when waiting for UserAppServer
    # metadata to change state.
    MAX_SLEEP_TIME = 30

    # Max time to wait to see if an application is uploaded.
    MAX_WAIT_TIME = 60 * 60  # 1 hour.

    MY_PUBLIC_IP = UA_SERVER_IP

    UA_SERVER_IP = UA_SERVER_IP

    # The port that the UserAppServer runs on, by default.
    UA_SERVER_PORT = 4343

    # A regular expression that can be used to find out from the user's data in
    # the UserAppServer if they are a cloud-level administrator in this AppScale
    # cloud.
    CLOUD_ADMIN_REGEX = "is_cloud_admin:true"

    # A regular expression that can be used to get the user's nickname (everything
    # preceding the initial '@' symbol) from their e-mail address.
    USERNAME_FROM_EMAIL_REGEX = '\A(.*)@'

    # A regular expression that can be used to retrieve the SHA1-hashed password
    # stored in a user's data with the UserAppServer.
    USER_DATA_PASSWORD_REGEX = 'password:([0-9a-fA-F]+)'

    # A regular expression that can be used to see if the given user is actually
    # a valid user in our system. This is useful in cases when the UserAppServer
    # returns error messages instead of user names.
    ALL_USERS_NON_USER_REGEX = '^[_]+$'

    MIN_PASSWORD_LENGTH = 6

    # Regular expression that matches email addresses.
    USER_EMAIL_REGEX = '^\w[^@\s]*@[^@\s]{2,}$'

    def __init__(self):
        """Creates a new UserAppClient.

        Args:
          host: The location where an UserAppClient can be found.
          secret: A str containing the secret key, used to authenticate this client
            when talking to remote UserAppServers.
        """
        self.host = self.UA_SERVER_IP
        self.server = SOAPpy.SOAPProxy('https://%s:%s' % (self.host, self.PORT))
        self.secret = LocalState.get_secret_key(KEY_NAME)

        # Disable certificate verification for Python 2.7.9.
        if hasattr(ssl, '_create_unverified_context'):
            print "Disabling certificate verification for Python 2.7.9"
            ssl._create_default_https_context = ssl._create_unverified_context

    def create_user(self, username, password, account_type='xmpp_user'):
        """Creates a new user account, with the given username and hashed password.

        Args:
          username: An e-mail address that should be set as the new username.
          password: A sha1-hashed password that is bound to the given username.
          account_type: A str that indicates if this account can be logged into by
            XMPP users.
        """

        encrypted_pass = LocalState.encrypt_password(username, password)
        # xmpp_pass = LocalState.encrypt_password(xmpp_user, password)
        print ("Creating new user account {0}".format(username))
        while 1:
            try:
                result = self.server.commit_new_user(username, encrypted_pass, account_type,
                                                     self.secret)
                return result
            except Exception, exception:
                print ("Exception when creating user: {0}".format(exception))
                print ("Backing off and trying again")
                time.sleep(10)

        if result != 'true':
            raise Exception(result)

    def get_user_data(self, username):
        print ("Retrieving user account {0}".format(username))
        while 1:
            try:
                result = self.server.get_user_data(username, self.secret)
                return result
            except Exception, exception:
                print ("Exception when retrieving user: {0}".format(exception))
                print ("Backing off and trying again")
                time.sleep(10)

        if not result:
            raise Exception(result)

    def get_all_users(self, secret):
        return True

    def delete_user(self, username):
        print ("Deleting user account {0}".format(username))
        while 1:
            try:
                result = self.server.delete_user(username, self.secret)
                break
            except Exception, exception:
                print ("Exception when deleting user: {0}".format(exception))
                print ("Backing off and trying again")
                time.sleep(10)

        if result != 'true':
            raise Exception(result)

    def delete_all_users(self):
        print ("Deleting all users account")
        while 1:
            try:
                result = self.server.delete_all_users(self.secret)
                break
            except Exception, exception:
                print ("Exception when deleting all users: {0}".format(exception))
                print ("Backing off and trying again")
                time.sleep(10)

        if result != 'true':
            raise Exception(result)

    def set_admin_role(self, username):
        """Grants the given user the ability to perform any administrative action.

        Args:
          username: The e-mail address that should be given administrative
            authorizations.
        """
        print ('Granting admin privileges to %s' % username)
        self.server.set_cloud_admin_status(username, 'true', self.secret)
        self.server.set_capabilities(username, self.ADMIN_CAPABILITIES, self.secret)

    def does_user_exist(self, username, silent=False):
        """Queries the UserAppServer to see if the given user exists.

        Returns:
          True if the given user exists, False otherwise.
        """

        while 1:
            try:
                if self.server.does_user_exist(username, self.secret) == "true":
                    return True
                else:
                    return False
            except Exception, exception:
                if not silent:
                    print ("Exception when checking if a user exists: {0}". \
                           format(exception))
                    print ("Backing off and trying again")
                time.sleep(10)

    def change_password(self, username, password):
        """Sets the given user's password to the specified (hashed) value.

        Args:
          username: The e-mail address for the user whose password will be
            changed.
          password: The SHA1-hashed password that will be set as the user's
            password.
        """
        result = self.server.change_password(username, password, self.secret)
        if result != 'true':
            raise Exception(result)
        return True

    def is_user_enabled(self, user, secret):
        return self.server.is_user_enabled(user, secret)

    def enable_user(self, user, secret):
        # enable_user(user, secret)
        return True

    def disable_user(self, username):
        print ("Disabling user account {0}".format(username))
        while 1:
            try:
                result = self.server.disable_user(username, self.secret)
                break
            except Exception, exception:
                print ("Exception when disabling user: {0}".format(exception))
                print ("Backing off and trying again")
                time.sleep(10)

        if result != 'true':
            raise Exception(result)

    def parse_new_user_post(self, email, password, password_confirmation):
        """ Parse the input from the create user form.

        Returns:
          A dict that maps the form fields on the user creation page to None (if
            they pass our validation) or a str indicating why they fail our
            validation.
        """
        users = {}
        error_msgs = {}
        users['email'] = cgi.escape(email)
        if re.match(self.USER_EMAIL_REGEX, users['email']):
            error_msgs['email'] = None
        else:
            error_msgs['email'] = 'Format must be foo@boo.goo.'

        users['password'] = cgi.escape(password)
        if len(users['password']) >= self.MIN_PASSWORD_LENGTH:
            error_msgs['password'] = None
        else:
            error_msgs['password'] = 'Password must be at least {0} characters ' \
                                     'long.'.format(self.MIN_PASSWORD_LENGTH)

        users['password_confirmation'] = cgi.escape(password_confirmation)
        if users['password_confirmation'] == users['password']:
            error_msgs['password_confirmation'] = None
        else:
            error_msgs['password_confirmation'] = 'Passwords do not match.'

        return error_msgs
