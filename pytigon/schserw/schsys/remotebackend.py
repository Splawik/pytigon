"""Module containing the RemoteUserBackendMod class for Apache authorization."""

from django.contrib.auth.backends import RemoteUserBackend


class RemoteUserBackendMod(RemoteUserBackend):
    """Backend for apache authorization"""

    def clean_username(self, username):
        """
        Clean the username by replacing backslashes with underscores and converting to lowercase.

        Args:
            username (str): The username to clean, typically in the format 'domain\\user'.

        Returns:
            str: The cleaned username in the format 'domain_user'.

        Raises:
            TypeError: If the username is not a string.
        """
        if not isinstance(username, str):
            raise TypeError("Username must be a string.")

        return username.lower().replace("\\", "_").strip()
