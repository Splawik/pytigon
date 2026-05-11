"""
Pytest tests for pytigon.schserw.schsys.remotebackend module.
"""

import pytest
from pytigon.schserw.schsys.remotebackend import RemoteUserBackendMod


class TestRemoteUserBackendMod:
    def test_clean_username_simple(self):
        """Test clean_username with a simple username."""
        backend = RemoteUserBackendMod()
        result = backend.clean_username("TestUser")
        assert result == "testuser"

    def test_clean_username_with_domain(self):
        """Test clean_username with domain\\username format."""
        backend = RemoteUserBackendMod()
        result = backend.clean_username("DOMAIN\\User")
        assert result == "domain_user"

    def test_clean_username_with_multiple_backslashes(self):
        """Test clean_username with multiple backslashes."""
        backend = RemoteUserBackendMod()
        result = backend.clean_username("DOMAIN\\Sub\\User")
        assert result == "domain_sub_user"

    def test_clean_username_with_whitespace(self):
        """Test clean_username with leading/trailing whitespace."""
        backend = RemoteUserBackendMod()
        result = backend.clean_username("  User  ")
        assert result == "user"

    def test_clean_username_lowercase(self):
        """Test that clean_username converts to lowercase."""
        backend = RemoteUserBackendMod()
        result = backend.clean_username("UPPERCASE")
        assert result == "uppercase"

    def test_clean_username_mixed_case_and_domain(self):
        """Test clean_username with mixed case and domain backslash."""
        backend = RemoteUserBackendMod()
        result = backend.clean_username("MyDomain\\MyUser")
        assert result == "mydomain_myuser"

    def test_clean_username_no_backslash(self):
        """Test clean_username without backslash."""
        backend = RemoteUserBackendMod()
        result = backend.clean_username("simpleuser")
        assert result == "simpleuser"

    def test_clean_username_empty_string(self):
        """Test clean_username with empty string."""
        backend = RemoteUserBackendMod()
        result = backend.clean_username("")
        assert result == ""

    def test_clean_username_non_string_raises_typeerror(self):
        """Test clean_username raises TypeError for non-string input."""
        backend = RemoteUserBackendMod()
        with pytest.raises(TypeError, match="Username must be a string"):
            backend.clean_username(123)

    def test_clean_username_none_raises_typeerror(self):
        """Test clean_username raises TypeError for None input."""
        backend = RemoteUserBackendMod()
        with pytest.raises(TypeError, match="Username must be a string"):
            backend.clean_username(None)
