#!/usr/bin/env python
# Programmer: Chris Bunch, Brian Drawert


# First-party Python imports
import hashlib
import json
import os

# AppScale-specific imports
from custom_exceptions import AppScaleException
# from custom_exceptions import BadConfigurationException

# /root/.appscale/locations-appscalee84eec16c3f8410896423d6424f998e2.json
LOCAL_APPSCALE_PATH = "/root/.appscale" + os.sep


class LocalState(object):
    """LocalState handles all interactions necessary to read and write AppScale
    configuration files on the machine that executes the AppScale Tools.
    """

    # The number of times to execute shell commands before aborting, by default.
    DEFAULT_NUM_RETRIES = 5

    # The path on the local filesystem where we can read and write
    # AppScale deployment metadata.
    # LOCAL_APPSCALE_PATH = os.path.expanduser("~") + os.sep + ".appscale" + os.sep

    # The length of the randomly generated secret that is used to authenticate
    # AppScale services.
    SECRET_KEY_LENGTH = 32

    # The username for the cloud administrator if the --test options is used.
    DEFAULT_USER = "a@a.com"

    # The password to set for the default user.
    DEFAULT_PASSWORD = "aaaaaa"

    @classmethod
    def encrypt_password(cls, username, password):
        """Salts the given password with the provided username and encrypts it.

        Args:
          username: A str representing the username whose password we wish to
            encrypt.
          password: A str representing the password to encrypt.
        Returns:
          The SHA1-encrypted password.
        """
        return hashlib.sha1(username + password).hexdigest()

    @classmethod
    def get_login_host(cls, keyname):
        """Searches through the local metadata to see which virtual machine runs the
        login service.

        Args:
          keyname: The SSH keypair name that uniquely identifies this AppScale
            deployment.
        Returns:
          A str containing the host that runs the login service.
        """
        return cls.get_host_with_role(keyname, 'login')

    @classmethod
    def get_host_with_role(cls, keyname, role):
        """Searches through the local metadata to see which virtual machine runs the
        specified role.

        Args:
          keyname: The SSH keypair name that uniquely identifies this AppScale
            deployment.
          role: A str indicating the role to search for.
        Returns:
          A str containing the host that runs the specified service.
        """
        nodes = cls.get_local_nodes_info(keyname)
        for node in nodes:
            if role in node['jobs']:
                return node['public_ip']
        raise AppScaleException("Couldn't find a {0} node.".format(role))

    @classmethod
    def get_local_nodes_info(cls, keyname):
        """Reads the JSON-encoded metadata on disk and returns a list that indicates
        which machines run each API service in this AppScale deployment.

        Args:
          keyname: A str that represents an SSH keypair name, uniquely identifying
            this AppScale deployment.
        Returns:
          A list of dicts, where each dict contains information on a single machine
          in this AppScale deployment.
        Raises:
          BadConfigurationException: If there is no JSON-encoded metadata file
            named after the given keyname.
        """
        # if not os.path.exists(cls.get_locations_json_location(keyname)):
        #    raise BadConfigurationException("AppScale does not appear to be " + \
        #                                    "running with keyname {0}".format(keyname))

        with open(cls.get_locations_json_location(keyname), 'r') as file_handle:
            return json.loads(file_handle.read())

    @classmethod
    def get_locations_json_location(cls, keyname):
        """Determines the location where the JSON file can be found that contains
        information related to service placement (e.g., where machines can be found
        and what services they run).

        Args:
          keyname: A str that indicates the name of the SSH keypair that
            uniquely identifies this AppScale deployment.
        Returns:
          A str that indicates where the locations.json file can be found.
        """
        return LOCAL_APPSCALE_PATH + "locations-" + keyname + ".json"

    @classmethod
    def get_all_public_ips(cls, keyname):
        """Searches through the local metadata to get all of the public IPs or FQDNs
        for machines in this AppScale deployment.

        Args:
          keyname: The SSH keypair name that uniquely identifies this AppScale
            deployment.
        Returns:
          A list containing all the public IPs or FQDNs in this AppScale deployment.
        """
        nodes = cls.get_local_nodes_info(keyname)
        return [node['public_ip'] for node in nodes]

    @classmethod
    def get_secret_key(cls, keyname):
        """Retrieves the secret key, used to authenticate AppScale services.

        Args:
          keyname: A str representing the SSH keypair name used for this AppScale
            deployment.
        Returns:
          A str containing the secret key.
        """
        with open(cls.get_secret_key_location(keyname), 'r') as file_handle:
            return file_handle.read()

    @classmethod
    def get_secret_key_location(cls, keyname):
        """Returns the path on the local filesystem where the secret key can be
        located.

        Args:
          keyname: A str representing the SSH keypair name used for this AppScale
            deployment.
        Returns:
          A str that corresponds to a location on the local filesystem where the
          secret key can be found.
        """
        return LOCAL_APPSCALE_PATH + keyname + ".secret"

