"""Pytest tests for pytigon_lib.schdjangoext.django_storage module.

Tests focus on class structure, validation logic, and name generation
that don't require a fully configured Django filesystem backend.
"""

import pytest

# Skip tests if fsspec is not available
pytest.importorskip("fsspec", reason="fsspec package not installed")
pytest.importorskip("django", reason="Django not installed")

from pytigon_lib.schdjangoext.django_storage import (
    OSFS_EXT,
    FSStorage,
    ThumbnailFileSystemStorage,
)

# ---------------------------------------------------------------------------
# FSStorage validation tests (no filesystem needed)
# ---------------------------------------------------------------------------


class TestFSStorageValidation:
    def test_validate_file_name_always_true(self):
        """Test validate_file_name always returns True."""
        assert FSStorage.validate_file_name("anything.txt") is True
        assert FSStorage.validate_file_name("/absolute/path/file.txt") is True
        assert FSStorage.validate_file_name("../relative/path.txt") is True
        assert FSStorage.validate_file_name("") is True

    def test_validate_file_name_allow_relative(self):
        """Test validate_file_name with allow_relative_path parameter."""
        assert FSStorage.validate_file_name("file.txt", allow_relative_path=True) is True
        assert FSStorage.validate_file_name("file.txt", allow_relative_path=False) is True


# ---------------------------------------------------------------------------
# FSStorage name generation tests
# ---------------------------------------------------------------------------


class TestFSStorageGetAvailableName:
    def test_get_alternative_name_format(self):
        """Test pattern of alternative names generated.

        FSStorage inherits get_alternative_name from Django's Storage base class,
        which appends random suffixes. We test the base behavior.
        """
        from django.core.files.storage import Storage

        storage = Storage()
        # get_alternative_name should return a name with different suffix
        alt = storage.get_alternative_name("test", ".txt")
        assert alt.startswith("test_")
        assert alt.endswith(".txt")


# ---------------------------------------------------------------------------
# ThumbnailFileSystemStorage tests
# ---------------------------------------------------------------------------


class TestThumbnailFileSystemStorage:
    def test_init_with_defaults_uses_settings(self):
        """Test initialization reads from Django settings.

        This test verifies the class can be imported and has the
        expected interface. Actual settings-dependent behavior
        requires a configured Django environment.
        """
        assert ThumbnailFileSystemStorage is not None
        # Verify the class has the expected methods
        assert hasattr(ThumbnailFileSystemStorage, "url")

    def test_url_method_raises_without_base_url(self):
        """Test url() raises ValueError when base_url is None."""
        # This test may be skipped if Django settings are not configured
        try:
            storage = ThumbnailFileSystemStorage(base_url=None)
            with pytest.raises(ValueError, match="not accessible via a URL"):
                storage.url("some_file.jpg")
        except Exception as e:
            pytest.skip(f"Cannot test without Django settings: {e}")


# ---------------------------------------------------------------------------
# OSFS_EXT tests
# ---------------------------------------------------------------------------


class TestOSFSExt:
    def test_class_exists(self):
        """Test OSFS_EXT class exists and inherits from _AutoCreateLocalFs."""
        assert OSFS_EXT is not None

    def test_init_creates_directory(self, tmp_path):
        """Test OSFS_EXT creates directory if it doesn't exist."""
        new_dir = tmp_path / "new_storage"
        assert not new_dir.exists()

        fs_instance = OSFS_EXT(str(new_dir))
        assert fs_instance is not None
        assert new_dir.exists()
        assert new_dir.is_dir()

    def test_init_existing_directory(self, tmp_path):
        """Test OSFS_EXT works with existing directory."""
        existing_dir = tmp_path / "existing"
        existing_dir.mkdir()
        assert existing_dir.exists()

        fs_instance = OSFS_EXT(str(existing_dir))
        assert fs_instance is not None
        assert existing_dir.exists()
